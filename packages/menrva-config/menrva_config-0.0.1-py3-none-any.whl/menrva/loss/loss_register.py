from copy import deepcopy
from typing import (
    Any,
    TypedDict,
    Dict,
    List,
    Union,
    Optional,
    Literal,
    Tuple,
    Callable,
    Type,
)
from typing_extensions import NotRequired
import importlib
import inspect
from collections import defaultdict
import warnings
import sys
from pathlib import Path


__all__ = ["LossRegister", "ComposedLoss", "Loss"]


class FullLossCfg(TypedDict):
    name: str
    weight: NotRequired[float]
    target: NotRequired[str]
    args: NotRequired[Dict[str, Any]]


class Loss:
    name: str
    backend: str

    def __init__(self, **kwargs):
        self.other_args = kwargs

    def __call__(*args, **kwargs):
        raise NotImplementedError

    def get_params(self) -> Dict[str, Any]:
        return self.other_args

    def __repr__(self):
        repr = self.name
        if self.other_args:
            repr = (
                repr
                + "["
                + ",".join([f"{n}={v}" for n, v in self.other_args.items()])
                + "]"
            )
        return repr


class LossRegister:
    # choose the backend
    def __init__(self, *, backend: Literal["torch"] = "torch"):
        self.backend = backend
        self.losses = []

        if self.backend not in ["torch"]:
            warnings.warn(f"using not standard backend {backend}", UserWarning)

        if self.backend == "torch":
            try:
                from .torch import L1, L2, CrossEntropy
            except ImportError:
                raise ImportError("required backend torch but torch isn't installed")

            self.register(L1, L2, CrossEntropy)

    # register available losses
    def register(self, *losses: Type[Loss]):
        for loss in losses:
            if loss.backend != self.backend:
                raise ValueError(
                    f"loss {loss} has backend {loss.backend} but register {self.backend}"
                )
            self.losses.append(loss)

    def register_from_module(
        self, module_name: str, base_path: Union[Path, str, None] = None, 
    ):
        """
        Finds all the loss functions in a module and returns them
        """
        try:
            if base_path is not None:
                sys.path.append(base_path)

            mod = importlib.import_module(module_name)
            found = inspect.getmembers(
                mod, lambda x: inspect.isclass(x) and issubclass(x, Loss) and x != Loss
                and x.backend == self.backend,
            )
            found = [v[1] for v in found]
            self.register(*found)
        except ModuleNotFoundError:
            pass
        
        finally:
            if base_path is not None:
                sys.path.remove(base_path)

    # select used losses and output the Loss object

    def build(self, cfg: Union[str, List[str], List[FullLossCfg]]) -> "ComposedLoss":
        losses = {loss_fn.name: loss_fn for loss_fn in self.losses}

        if isinstance(cfg, str):
            loss_fn = losses[cfg]()
            composed_losses = [(1.0, None, loss_fn)]
        elif isinstance(cfg, list):
            composed_losses = []
            for loss in cfg:
                if isinstance(loss, str):
                    loss_fn = losses[loss]()
                    composed_losses.append((1.0, None, loss_fn))
                else:
                    loss_fn = losses[loss["name"]]
                    composed_losses.append(
                        (
                            loss.get("weight", 1.0),
                            loss.get("target", None),
                            loss_fn(**loss.get("args", {})),
                        )
                    )
        else:
            raise ValueError(f"not recognized cfg {cfg}")

        return ComposedLoss(composed_losses)


class ComposedLoss:
    def __init__(self, losses: List[Tuple[float, Optional[str], Callable]]):
        self._losses = losses
        self._targets = list({l[1] for l in losses})

    @property
    def targets(self):
        return self._targets

    def update_loss_params(
        self, loss_name: str, loss_target: Optional[str] = None, **kwargs
    ):
        """
        Update some parameters for a specific loss, if the indicated loss is
        not present this function does not do nothing
        """
        for _, target, loss in self._losses:
            if loss.name == loss_name and target == loss_target:
                loss.other_args.update(**kwargs)

    def __call__(
        self,
        *,
        pred: Optional[Any] = None,
        gt: Optional[Any] = None,
        target: Optional[str] = None,
        **kwargs,
    ):
        losses_filtered = [(w, l) for w, t, l in self._losses if t == target]
        if not losses_filtered:
            warnings.warn(
                f"no losses found for target '{target}', output loss 0.0",
                category=RuntimeWarning,
            )

        out = 0.0
        for weight, loss in losses_filtered:
            out += weight * loss(pred=pred, gt=gt, **kwargs, **loss.other_args)
        return out

    def __repr__(self):
        if len(self._losses) == 1:
            w, _, loss = self._losses[0]
            return str(w) + str(loss) if w != 1.0 else str(loss)
        else:
            return "+".join(
                [f"{w if w != 1.0 else ''}{str(loss)}" for w, _, loss in self._losses]
            )

    def split_by_target(self) -> "Dict[str, Loss]":
        targets = {t for w, t, l in self._losses}
        losses = {}
        for t in targets:
            _loss_copy = deepcopy(self)
            _loss_copy._losses = [deepcopy(l) for l in self._losses if l[1] == t]
            losses[t] = _loss_copy
        return losses

    def get_params(self) -> Dict[Any, Any]:
        params = defaultdict(lambda: {})
        for weight, target, loss in self._losses:
            if target is None:
                params[loss.name] = {
                    "weight": weight,
                    **loss.get_params()
                }
            else:
                params[target][loss.name] = {
                    "weight": weight,
                    **loss.get_params()
                }
        return params