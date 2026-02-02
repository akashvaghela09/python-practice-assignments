import importlib
import io
import contextlib
import inspect
import pytest

MODULE_NAME = "03_defaultParameter"


def load_module_capture_output():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def test_stdout_exact():
    mod, out = load_module_capture_output()
    expected = "7\n15\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_add_signature_and_defaults():
    mod = importlib.reload(importlib.import_module(MODULE_NAME))
    assert hasattr(mod, "add")
    sig = inspect.signature(mod.add)
    params = list(sig.parameters.values())

    assert len(params) == 2, f"expected={2!r} actual={len(params)!r}"
    assert params[0].name == "a", f"expected={'a'!r} actual={params[0].name!r}"
    assert params[1].name == "b", f"expected={'b'!r} actual={params[1].name!r}"
    expected_default = 5
    actual_default = params[1].default
    assert actual_default == expected_default, f"expected={expected_default!r} actual={actual_default!r}"


@pytest.mark.parametrize(
    "args, expected",
    [
        ((2,), 7),
        ((10,), 15),
        ((2, 1), 3),
        ((-3,), 2),
        ((0, 0), 0),
        ((1.5,), 6.5),
    ],
)
def test_add_behavior(args, expected):
    mod = importlib.reload(importlib.import_module(MODULE_NAME))
    actual = mod.add(*args)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"