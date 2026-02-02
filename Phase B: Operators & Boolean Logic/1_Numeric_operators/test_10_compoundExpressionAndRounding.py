import importlib.util
import os
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext

import pytest


MODULE_FILENAME = "10_compoundExpressionAndRounding.py"


def load_module():
    test_dir = os.path.dirname(__file__)
    module_path = os.path.join(test_dir, MODULE_FILENAME)
    if not os.path.exists(module_path):
        module_path = os.path.abspath(MODULE_FILENAME)

    spec = importlib.util.spec_from_file_location("student_mod_10", module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def compute_expected(price, qty, discount_percent, tax_percent):
    getcontext().prec = 28
    p = Decimal(str(price))
    q = Decimal(str(qty))
    d = Decimal(str(discount_percent)) / Decimal("100")
    t = Decimal(str(tax_percent)) / Decimal("100")
    subtotal = p * q
    discount_amount = subtotal * d
    after_discount = subtotal - discount_amount
    tax_amount = after_discount * t
    final_total = after_discount + tax_amount
    return final_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def test_final_total_value_is_correct():
    mod = load_module()
    expected = float(compute_expected(mod.price, mod.qty, mod.discount_percent, mod.tax_percent))
    actual = mod.final_total
    assert actual == expected, f"expected={expected} actual={actual}"


def test_final_total_is_rounded_to_two_decimals():
    mod = load_module()
    expected = float(compute_expected(mod.price, mod.qty, mod.discount_percent, mod.tax_percent))
    actual = mod.final_total
    assert isinstance(actual, (int, float)), f"expected={type(expected)} actual={type(actual)}"
    assert round(actual, 2) == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_expected(monkeypatch, capsys):
    mod = load_module()
    expected_total = float(compute_expected(mod.price, mod.qty, mod.discount_percent, mod.tax_percent))
    print("Final total:", mod.final_total)
    out = capsys.readouterr().out
    expected_out = f"Final total: {expected_total}\n"
    assert out == expected_out, f"expected={expected_out!r} actual={out!r}"