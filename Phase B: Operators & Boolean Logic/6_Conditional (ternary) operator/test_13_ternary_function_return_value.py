import importlib
import contextlib
import io
import pytest

MODULE_NAME = "13_ternary_function_return_value"


def load_module():
    mod = importlib.import_module(MODULE_NAME)
    return mod


def test_import_prints_expected_output():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(MODULE_NAME))
    out = buf.getvalue()
    expected = "fizz\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


@pytest.mark.parametrize(
    "x, expected",
    [
        (9, "fizz"),
        (3, "fizz"),
        (0, "fizz"),
        (6, "fizz"),
        (-3, "fizz"),
        (1, "1"),
        (2, "2"),
        (4, "4"),
        (10, "10"),
        (-1, "-1"),
        (-2, "-2"),
        (-4, "-4"),
    ],
)
def test_fizz_or_number_values(x, expected):
    mod = load_module()
    actual = mod.fizz_or_number(x)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_fizz_or_number_returns_str_type():
    mod = load_module()
    actual = mod.fizz_or_number(5)
    assert isinstance(actual, str), f"expected={str!r} actual={type(actual)!r}"