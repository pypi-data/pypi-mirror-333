import torch  # type: ignore
from torch.nn import functional as F   # type: ignore
from typing import List, Union
from .loss_register import Loss

__all__ = [
    "TorchLoss",
    "L1",
    "L2",
    "CrossEntropy",
]


class TorchLoss(Loss):
    backend = "torch"


class L1(TorchLoss):
    name = "l1"

    def __call__(self, pred: torch.Tensor, gt: torch.Tensor, **kwargs):
        return torch.mean(torch.abs(pred - gt))


class L2(TorchLoss):
    name = "l2"

    def __call__(self, pred: torch.Tensor, gt: torch.Tensor, **kwargs):
        return torch.mean(torch.square(pred - gt))


# classification


class CrossEntropy(TorchLoss):
    name = "cross_entropy"

    def __call__(
        self,
        pred: torch.Tensor,
        gt: torch.Tensor,
        weight: Union[List[float], None] = None,
        **kwargs,
    ):
        if isinstance(weight, list):
            weight = torch.tensor(weight, dtype=pred.dtype, device=gt.device)
        return F.cross_entropy(pred, gt, weight=weight)
