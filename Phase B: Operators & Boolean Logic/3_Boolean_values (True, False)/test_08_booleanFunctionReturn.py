import importlib.util
import os
import types
import pytest

ASSIGNMENT_FILE = "08_booleanFunctionReturn.py"


def load_module_from_file(path):
    spec = importlib.util.spec_from_file_location("assignment08", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def mod():
    path = os.path.join(os.path.dirname(__file__), ASSIGNMENT_FILE)
    return load_module_from_file(path)


@pytest.mark.parametrize(
    "n, expected",
    [
        (10, True),
        (7, False),
        (0, True),
        (-2, True),
        (-3, False),
        (2**31 - 1, False),
        (2**31 - 2, True),
    ],
)
def test_is_even_basic(mod, n, expected):
    actual = mod.is_even(n)
    assert actual is expected, f"expected={expected} actual={actual}"


@pytest.mark.parametrize("n", [10, 7, 0, -2, -3, 2, 1, 100, 101])
def test_is_even_returns_bool(mod, n):
    actual = mod.is_even(n)
    assert isinstance(actual, bool), f"expected={bool} actual={type(actual)}"


def test_is_even_rejects_non_int_like(mod):
    with pytest.raises(TypeError):
        mod.is_even("10")


def test_is_even_accepts_bool_as_int(mod):
    assert mod.is_even(True) is False, "expected=False actual=True"
    assert mod.is_even(False) is True, "expected=True actual=False"