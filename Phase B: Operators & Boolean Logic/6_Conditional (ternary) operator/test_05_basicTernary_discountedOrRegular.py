import importlib
import io
import sys
import pytest


MODULE_NAME = "05_basicTernary_discountedOrRegular"


def run_module_capture_stdout():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        mod = importlib.import_module(MODULE_NAME)
    finally:
        sys.stdout = old
    return mod, buf.getvalue()


def test_prints_exact_output():
    _, out = run_module_capture_stdout()
    expected = "final=45.0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_final_price_value():
    mod, _ = run_module_capture_stdout()
    expected = 45.0
    actual = getattr(mod, "final_price", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_ternary_expression():
    mod, _ = run_module_capture_stdout()
    expected = mod.price * 0.9
    actual = mod.final_price
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_not_callables_or_placeholders():
    mod, _ = run_module_capture_stdout()
    actual = mod.final_price
    expected = False
    assert callable(actual) == expected, f"expected={expected!r} actual={callable(actual)!r}"