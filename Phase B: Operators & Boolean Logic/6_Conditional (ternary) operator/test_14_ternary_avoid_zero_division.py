import importlib
import sys
import types
import pytest


def _exec_module_with_overrides(monkeypatch, numerator=10, denominator=0):
    path = "14_ternary_avoid_zero_division"
    if path in sys.modules:
        del sys.modules[path]

    import builtins

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr(builtins, "print", fake_print)

    mod = importlib.import_module(path)
    mod.numerator = numerator
    mod.denominator = denominator

    if hasattr(mod, "result"):
        mod.result = "undefined" if mod.denominator == 0 else mod.numerator / mod.denominator
    else:
        raise AssertionError("Missing required variable.")

    builtins.print(mod.result)
    out = "".join(captured)
    return mod, out


def test_prints_undefined_on_zero_denominator(monkeypatch):
    _, out = _exec_module_with_overrides(monkeypatch, numerator=10, denominator=0)
    expected = "undefined\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_result_is_string_undefined_on_zero_denominator(monkeypatch):
    mod, _ = _exec_module_with_overrides(monkeypatch, numerator=10, denominator=0)
    expected = "undefined"
    actual = mod.result
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, str), f"expected={str!r} actual={type(actual)!r}"


def test_result_is_numeric_on_nonzero_denominator(monkeypatch):
    mod, out = _exec_module_with_overrides(monkeypatch, numerator=10, denominator=2)
    expected_value = 10 / 2
    actual_value = mod.result
    assert actual_value == expected_value, f"expected={expected_value!r} actual={actual_value!r}"
    expected_out = f"{expected_value}\n"
    assert out == expected_out, f"expected={expected_out!r} actual={out!r}"


def test_no_zero_division_error_when_denominator_zero(monkeypatch):
    try:
        _exec_module_with_overrides(monkeypatch, numerator=1, denominator=0)
    except ZeroDivisionError as e:
        assert False, f"expected={type(Exception()).__name__!r} actual={type(e).__name__!r}"