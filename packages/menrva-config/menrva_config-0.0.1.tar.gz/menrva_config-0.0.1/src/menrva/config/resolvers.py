"""
OmegaConf utility resolvers
"""
from typing import Callable, Dict

__all__ = ["extra_resolvers"]


def extra_resolvers() -> Dict[str, Callable]:
    return {"eval": eval}
