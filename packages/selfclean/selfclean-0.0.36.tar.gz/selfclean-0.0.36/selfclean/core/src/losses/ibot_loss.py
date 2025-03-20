import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch import nn


class iBOTLoss(nn.Module):
    def __init__(
        self,
        out_dim: int,
        patch_out_dim: int,
        n_g_crops: int,
        n_l_crops: int,
        warmup_teacher_temp: float,
        teacher_temp: float,
        warmup_teacher_patch_temp: float,
        teacher_patch_temp: float,
        warmup_teacher_temp_epochs: int,
        n_epochs: int,
        student_temp: float = 0.1,
        center_momentum: float = 0.9,
        center_momentum2: float = 0.9,
        lambda1: float = 1.0,
        lambda2: float = 1.0,
        mim_start_epoch: int = 0,
    ):
        super().__init__()
        warmup_teacher_temp_epochs = min(n_epochs, warmup_teacher_temp_epochs)
        self.student_temp = student_temp
        self.center_momentum = center_momentum
        self.center_momentum2 = center_momentum2
        self.n_g_crops = n_g_crops
        self.n_l_crops = n_l_crops
        self.n_crops = n_g_crops + n_l_crops
        self.register_buffer("center", torch.zeros(1, out_dim))
        self.register_buffer("center2", torch.zeros(1, 1, patch_out_dim))
        self.lambda1 = lambda1
        self.lambda2 = lambda2

        # we apply a warm up for the teacher temperature because
        # a too high temperature makes the training instable at the beginning
        self.teacher_temp_schedule = np.concatenate(
            (
                np.linspace(
                    warmup_teacher_temp, teacher_temp, warmup_teacher_temp_epochs
                ),
                np.ones(n_epochs - warmup_teacher_temp_epochs) * teacher_temp,
            )
        )
        self.teacher_temp2_schedule = (
            np.concatenate(
                (
                    np.linspace(
                        warmup_teacher_patch_temp,
                        teacher_patch_temp,
                        warmup_teacher_temp_epochs,
                    ),
                    np.ones(n_epochs - warmup_teacher_temp_epochs) * teacher_patch_temp,
                )
            )
            if mim_start_epoch == 0
            else np.concatenate(
                (
                    np.ones(mim_start_epoch) * warmup_teacher_patch_temp,
                    np.linspace(
                        warmup_teacher_patch_temp,
                        teacher_patch_temp,
                        warmup_teacher_temp_epochs,
                    ),
                    np.ones(n_epochs - warmup_teacher_temp_epochs - mim_start_epoch)
                    * teacher_patch_temp,
                )
            )
        )

    def forward(
        self, student_output, teacher_output, student_local_cls, student_mask, epoch
    ):
        """
        Cross-entropy between softmax outputs of the teacher and student networks.
        """
        student_cls, student_patch = student_output
        teacher_cls, teacher_patch = teacher_output

        if student_local_cls is not None:
            student_cls = torch.cat([student_cls, student_local_cls])

        # [CLS] and patch for global patches
        student_cls = student_cls / self.student_temp
        student_cls_c = student_cls.chunk(self.n_crops)
        student_patch = student_patch / self.student_temp
        student_patch_c = student_patch.chunk(self.n_g_crops)

        # teacher centering and sharpening
        temp = self.teacher_temp_schedule[epoch]
        temp2 = self.teacher_temp2_schedule[epoch]
        teacher_cls_c = F.softmax((teacher_cls - self.center) / temp, dim=-1)
        teacher_cls_c = teacher_cls_c.detach().chunk(self.n_g_crops)
        teacher_patch_c = F.softmax((teacher_patch - self.center2) / temp2, dim=-1)
        teacher_patch_c = teacher_patch_c.detach().chunk(self.n_g_crops)

        total_loss1, n_loss_terms1 = 0, 0
        total_loss2, n_loss_terms2 = 0, 0
        for q in range(len(teacher_cls_c)):
            for v in range(len(student_cls_c)):
                if v == q:
                    loss2 = torch.sum(
                        -teacher_patch_c[q] * F.log_softmax(student_patch_c[v], dim=-1),
                        dim=-1,
                    )
                    mask = student_mask[v].flatten(-2, -1)
                    loss2 = torch.sum(loss2 * mask.float(), dim=-1) / mask.sum(
                        dim=-1
                    ).clamp(min=1.0)
                    total_loss2 += loss2.mean()
                    n_loss_terms2 += 1
                else:
                    loss1 = torch.sum(
                        -teacher_cls_c[q] * F.log_softmax(student_cls_c[v], dim=-1),
                        dim=-1,
                    )
                    total_loss1 += loss1.mean()
                    n_loss_terms1 += 1

        total_loss1 = total_loss1 / n_loss_terms1 * self.lambda1
        total_loss2 = total_loss2 / n_loss_terms2 * self.lambda2
        total_loss = dict(
            cls=total_loss1, patch=total_loss2, loss=total_loss1 + total_loss2
        )
        self.update_center(teacher_cls, teacher_patch)
        return total_loss

    @torch.no_grad()
    def update_center(self, teacher_cls, teacher_patch):
        """
        Update center used for teacher output.
        """
        cls_center = torch.sum(teacher_cls, dim=0, keepdim=True)
        dist.all_reduce(cls_center)
        cls_center = cls_center / (len(teacher_cls) * dist.get_world_size())
        self.center = self.center * self.center_momentum + cls_center * (
            1 - self.center_momentum
        )

        patch_center = torch.sum(teacher_patch.mean(1), dim=0, keepdim=True)
        dist.all_reduce(patch_center)
        patch_center = patch_center / (len(teacher_patch) * dist.get_world_size())
        self.center2 = self.center2 * self.center_momentum2 + patch_center * (
            1 - self.center_momentum2
        )
