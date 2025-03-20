from typing import Optional, List, TypedDict, Dict, Any

class FullLrCfg(TypedDict):
    name: str
    cls: str
    optimizer: str
    args: Dict[str, Any]

class LrRegister:
    def __init__(self):
        self._registered = {}
        self._schedulers = []

    @property
    def schedulers(self):
        return [sc["scheduler"] for sc in self._schedulers]

    def register(self, name: str, scheduler):
        self._registered[name] = scheduler

    def register_torch_schedulers(self):
        from torch.optim import lr_scheduler  # type: ignore
        for label, cls in [
            ("step", lr_scheduler.StepLR),
            ("cosine_annealing", lr_scheduler.CosineAnnealingLR),
            ("cyclic", lr_scheduler.CyclicLR),
            ("reduce_on_plateau", lr_scheduler.ReduceLROnPlateau),
            ("multi_step_lr", lr_scheduler.MultiStepLR),
            ("one_cycle", lr_scheduler.OneCycleLR),
        ]:
            self.register(label, cls)

    def _add(
        self,
        name: str,
        optimizer,
        log_prefix: Optional[str] = None,
        **kwargs
    ):
        self._schedulers.append(
            {
                "scheduler": self._registered[name](optimizer, **kwargs),
                "log_prefix": log_prefix,
                "args": dict(**kwargs, **{"name": name}),
            }
        )

    def get_params(self):
        out = {}
        for sc in self._schedulers:
            to_log = sc["args"]
            if sc["log_prefix"] is not None:
                out.update({sc["log_prefix"] + "/" + k: v for k, v in to_log.items()})
            else:
                out.update(to_log)
        return out

    def build(self, conf: List[FullLrCfg], optimizers: dict):
        for sc_conf in conf:
            self._add(
                sc_conf["cls"],
                optimizers[sc_conf["optimizer"]],
                sc_conf["optimizer"] + "/" + sc_conf["name"],
                **sc_conf.get("args", {}),
            )