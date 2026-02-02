import importlib
import io
import contextlib
import builtins
import pytest

MODULE_NAME = "10_higher_order_function_applyTwice"


def load_module():
    if MODULE_NAME in list(importlib.sys.modules.keys()):
        del importlib.sys.modules[MODULE_NAME]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def test_prints_expected_output():
    _, out = load_module()
    expected = "5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_apply_twice_exists_and_callable():
    mod, _ = load_module()
    assert hasattr(mod, "apply_twice")
    assert callable(mod.apply_twice)


def test_increment_exists_and_callable():
    mod, _ = load_module()
    assert hasattr(mod, "increment")
    assert callable(mod.increment)


def test_increment_behavior():
    mod, _ = load_module()
    for n in [-2, -1, 0, 1, 2, 10]:
        expected = n + 1
        actual = mod.increment(n)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_apply_twice_calls_function_twice_and_returns_value():
    mod, _ = load_module()
    calls = {"n": 0}

    def f(x):
        calls["n"] += 1
        return x + 2

    value = 3
    expected = f(f(value))
    calls["n"] = 0
    actual = mod.apply_twice(f, value)
    assert calls["n"] == 2, f"expected={2!r} actual={calls['n']!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_apply_twice_with_increment():
    mod, _ = load_module()
    value = 7
    expected = value + 2
    actual = mod.apply_twice(mod.increment, value)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_apply_twice_with_non_numeric_value():
    mod, _ = load_module()

    def wrap(x):
        return [x]

    value = "a"
    expected = [[value]]
    actual = mod.apply_twice(wrap, value)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_apply_twice_propagates_exceptions():
    mod, _ = load_module()

    def boom(x):
        raise RuntimeError("err")

    with pytest.raises(RuntimeError):
        mod.apply_twice(boom, 1)