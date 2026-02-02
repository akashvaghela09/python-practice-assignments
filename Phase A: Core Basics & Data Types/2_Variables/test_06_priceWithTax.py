import importlib.util
import os
import sys
import pytest


def _load_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_exact_line(capsys):
    path = os.path.join(os.path.dirname(__file__), "06_priceWithTax.py")
    _load_module(path, "price_with_tax_mod")
    out = capsys.readouterr().out
    expected = "total=21.40\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_total_variable_present_and_correct(capsys):
    path = os.path.join(os.path.dirname(__file__), "06_priceWithTax.py")
    mod = _load_module(path, "price_with_tax_mod2")
    assert hasattr(mod, "total"), f"expected={True!r} actual={hasattr(mod, 'total')!r}"

    expected_total = mod.price + mod.price * mod.tax_rate
    actual_total = mod.total
    assert actual_total == pytest.approx(expected_total), f"expected={expected_total!r} actual={actual_total!r}"


def test_total_formatted_two_decimals(capsys):
    path = os.path.join(os.path.dirname(__file__), "06_priceWithTax.py")
    mod = _load_module(path, "price_with_tax_mod3")
    formatted = format(mod.total, ".2f")
    expected = "21.40"
    assert formatted == expected, f"expected={expected!r} actual={formatted!r}"