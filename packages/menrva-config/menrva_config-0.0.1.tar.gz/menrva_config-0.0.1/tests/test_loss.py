# tests about the loss register

from menrva.loss import LossRegister, Loss
from pathlib import Path
import pytest

# build fake losses for testing purposes


class MyL1(Loss):
    backend = "my-backend"
    name = "l1"

    def __call__(self, pred, gt, **kwargs):
        return abs(pred - gt)


class MyL2(Loss):
    backend = "my-backend"
    name = "l2"

    def __call__(self, pred, gt, **kwargs):
        return (pred - gt) ** 2


class WrongBackendL2(Loss):
    backend = "other-backend"
    name = "l2"

    def __call__(self, pred, gt, **kwargs):
        return (pred - gt) ** 2


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_register_loss():
    # test with correct engine
    register = LossRegister(backend="my-backend")
    register.register(MyL1, MyL2)

    # test with wrong engine
    with pytest.raises(ValueError):
        register = LossRegister(backend="my-backend")
        register.register(WrongBackendL2)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_load_module():
    register = LossRegister(backend="something")
    register.register_from_module(
        "custom_losses",
        str(Path(__file__).parent / "losses"),
    )
    for loss in register.losses:
        assert loss.backend == "something"
    assert len(register.losses) == 1


@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.parametrize(
    "cfg,output",
    [
        ("l1", 0.5),
        (["l1", "l2"], 0.75),
        ([{"name": "l1", "weight": 1.0}], 0.5),
        ([{"name": "l1", "weight": 0.5}], 0.25),
    ],
)
def test_build_and_call(cfg, output):
    register = LossRegister(backend="my-backend")
    register.register(MyL1, MyL2)
    composed_loss = register.build(cfg)
    err = composed_loss(pred=1.0, gt=0.5)
    assert err == output


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_call_targets():
    cfg = [
        {"name": "l1", "target": "fst_tgt"},
        {"name": "l1", "target": "snd_tgt"},
    ]
    register = LossRegister(backend="my-backend")
    register.register(MyL1, MyL2)
    composed_loss = register.build(cfg)

    err_fst = composed_loss(pred=1.0, gt=0.5, target="fst_tgt")
    assert err_fst == 0.5

    err_snd = composed_loss(pred=1.0, gt=0.5, target="snd_tgt")
    assert err_snd == 0.5


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_get_params():
    cfg = [
        {"name": "l1", "target": "fst_tgt", "args": {"a": 1}},
        {"name": "l1", "target": "snd_tgt", "args": {"b": 2}},
    ]
    register = LossRegister(backend="my-backend")
    register.register(MyL1, MyL2)
    composed_loss = register.build(cfg)
    cfg = composed_loss.get_params()
    assert cfg["fst_tgt"]["l1"]["a"] == 1
    assert cfg["snd_tgt"]["l1"]["b"] == 2