from typing import Any, Optional, List, Dict
from typing import TypedDict


class FullOptimCfg(TypedDict):
    name: str
    cls: str
    params: Dict[str, Any]
    args: Dict[str, Any]


class OptimRegister:
    def __init__(self):
        self._registered = {}
        self._optimizers = {}

    def register(self, label: str, optimizer):
        self._registered[label] = optimizer

    @property
    def optimizers(self) -> Dict[str, Any]:
        return {k: v["optimizer"] for k, v in self._optimizers.items()}

    def register_torch_optimizers(self):
        from torch import optim  # type: ignore

        for name, cls in [
            ("adam", optim.Adam),
            ("adamw", optim.AdamW),
            ("sgd", optim.SGD),
            ("rmsprop", optim.RMSprop),
        ]:
            self.register(name, cls)

    def _add(
        self,
        label: str,
        cls: str,
        params,
        log_prefix: Optional[str] = None,
        other_to_log: dict = {},
        **kwargs,
    ):
        self._optimizers[label] = {
            "name": label,
            "optimizer": self._registered[cls](params, **kwargs),
            "log_prefix": log_prefix,
            "args": dict(**kwargs, **{"name": cls}, **other_to_log),
        }

    def get_params(self):
        out = {}
        for opt in self._optimizers.values():
            if opt["log_prefix"] is not None:
                out.update(
                    {opt["log_prefix"] + "/" + k: v for k, v in opt["args"].items()}
                )
            else:
                out.update(opt["args"])
        return out

    def build(self, conf: List[FullOptimCfg], params: Dict[str, Any]):
        for op_conf in conf:
            other_to_log = {}
            self._add(
                op_conf["name"],
                op_conf["cls"],
                params[op_conf["params"]],
                log_prefix=op_conf["name"],
                **op_conf.get("args", {}),
                other_to_log=other_to_log,
            )
