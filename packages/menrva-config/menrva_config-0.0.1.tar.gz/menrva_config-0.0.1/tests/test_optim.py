## Build Fake Optimizer to test

from menrva.optim import OptimRegister, LrRegister
import pytest

try:
    import torch

    torch_available = True
except ImportError:
    torch_available = False

## Optimizer Tests


class FakeOptim:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_optim_register():
    optim = OptimRegister()
    optim.register("my_optim", FakeOptim)
    assert optim._registered["my_optim"] == FakeOptim


@pytest.mark.skipif(not torch_available, reason="pytorch not available")
def test_optim_build():
    # build the optimizer
    params = {"model": [torch.nn.Parameter(torch.randn(1, 1), requires_grad=True)]}
    config = [
        {"name": "my-adam", "cls": "adamw", "params": "model", "args": {"lr": 1e-4}},
        {"name": "snd-adam", "cls": "adamw", "params": "model", "args": {"lr": 1e-5}},
    ]

    optim = OptimRegister()
    optim.register_torch_optimizers()
    optim.build(config, params)

    # extract args
    expected_params = {
        "my-adam/lr": 1e-4,
        "my-adam/name": "adamw",
        "snd-adam/lr": 1e-5,
        "snd-adam/name": "adamw",
    }
    params = optim.get_params()
    assert params == expected_params


## Learning Rate Schedulers


class FakeScheduler:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_scheduler_register():
    optim = LrRegister()
    optim.register("my_scheduler", FakeScheduler)
    assert optim._registered["my_scheduler"] == FakeScheduler


@pytest.mark.skipif(not torch_available, reason="pytorch not available")
def test_scheduler_build():
    # build the optimizer
    optimizers = {
        "my-adam": torch.optim.Adam(
            [torch.nn.Parameter(torch.randn(1, 1), requires_grad=True)],
        )
    }
    config = [
        {
            "name": "scheduler",
            "cls": "multi_step_lr",
            "optimizer": "my-adam",
            "args": {
                "milestones": [60000, 90000],
                "gamma": 0.1,
            },
        },
    ]

    optim = LrRegister()
    optim.register_torch_schedulers()
    optim.build(config, optimizers)

    # extract args
    expected_params = {
        "my-adam/scheduler/gamma": 0.1,
        "my-adam/scheduler/milestones": [60000, 90000],
        "my-adam/scheduler/name": "multi_step_lr",
    }
    params = optim.get_params()
    assert params == expected_params


@pytest.mark.skipif(not torch_available, reason="pytorch not available")
def test_scheduler_optim_integration():
    # create optimizer
    params = {"model": [torch.nn.Parameter(torch.randn(1, 1), requires_grad=True)]}
    config = [
        {"name": "optimizer", "cls": "adamw", "params": "model", "args": {"lr": 1e-4}},
    ]
    optim = OptimRegister()
    optim.register_torch_optimizers()
    optim.build(config, params)

    config = [
        {
            "name": "scheduler",
            "cls": "multi_step_lr",
            "optimizer": "optimizer",
            "args": {
                "milestones": [60000, 90000],
                "gamma": 0.1,
            },
        },
    ]

    lroptim = LrRegister()
    lroptim.register_torch_schedulers()
    lroptim.build(config, optim.optimizers)

    # extract args
    expected_params = {
        "optimizer/scheduler/gamma": 0.1,
        "optimizer/scheduler/milestones": [60000, 90000],
        "optimizer/scheduler/name": "multi_step_lr",
    }
    params = lroptim.get_params()
    assert params == expected_params
