import importlib.util
import os
import sys
import types
import pytest


MODULE_FILENAME = "15_multiStepComputationWithReuse.py"
MODULE_NAME = "pricing_engine_15_multistep"


def _load_module_with_print_capture():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)

    captured = {"args": [], "kwargs": []}

    def fake_print(*args, **kwargs):
        captured["args"].append(args)
        captured["kwargs"].append(kwargs)

    module.__dict__["print"] = fake_print
    spec.loader.exec_module(module)
    return module, captured


@pytest.fixture(scope="module")
def mod_and_print():
    return _load_module_with_print_capture()


def test_import_prints_single_value(mod_and_print):
    _, cap = mod_and_print
    assert len(cap["args"]) == 1
    assert len(cap["args"][0]) == 1
    assert cap["args"][0][0] == 24.3


def test_subtotal_basic(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.subtotal([20, 5])
    expected = 25
    assert actual == expected, f"expected={expected} actual={actual}"


def test_subtotal_empty(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.subtotal([])
    expected = 0
    assert actual == expected, f"expected={expected} actual={actual}"


def test_discount_amount(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.discount_amount(25, 10)
    expected = 2.5
    assert actual == expected, f"expected={expected} actual={actual}"


def test_tax_amount(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.tax_amount(22.5, 8)
    expected = 1.8
    assert actual == expected, f"expected={expected} actual={actual}"


def test_final_total_matches_example(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.final_total([20, 5], 10, 8)
    expected = 24.3
    assert actual == expected, f"expected={expected} actual={actual}"


def test_final_total_no_discount_with_tax(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.final_total([10, 10], 0, 10)
    expected = 22.0
    assert actual == expected, f"expected={expected} actual={actual}"


def test_final_total_discount_no_tax(mod_and_print):
    mod, _ = mod_and_print
    actual = mod.final_total([10, 5], 20, 0)
    expected = 12.0
    assert actual == expected, f"expected={expected} actual={actual}"


def test_final_total_order_of_operations_via_spies(mod_and_print):
    mod, _ = mod_and_print

    calls = []

    original_subtotal = mod.subtotal
    original_discount = mod.discount_amount
    original_tax = mod.tax_amount

    def spy_subtotal(prices):
        calls.append(("subtotal", list(prices)))
        return original_subtotal(prices)

    def spy_discount(subtotal_value, percent):
        calls.append(("discount_amount", subtotal_value, percent))
        return original_discount(subtotal_value, percent)

    def spy_tax(amount, percent):
        calls.append(("tax_amount", amount, percent))
        return original_tax(amount, percent)

    mod.subtotal = spy_subtotal
    mod.discount_amount = spy_discount
    mod.tax_amount = spy_tax

    try:
        actual = mod.final_total([20, 5], 10, 8)
        expected = 24.3
        assert actual == expected, f"expected={expected} actual={actual}"
        assert [c[0] for c in calls] == ["subtotal", "discount_amount", "tax_amount"]
        assert calls[0][1] == [20, 5]
        assert calls[1][1] == 25
        assert calls[1][2] == 10
        assert calls[2][1] == 22.5
        assert calls[2][2] == 8
    finally:
        mod.subtotal = original_subtotal
        mod.discount_amount = original_discount
        mod.tax_amount = original_tax


def test_types_are_numeric(mod_and_print):
    mod, _ = mod_and_print
    assert isinstance(mod.subtotal([1, 2, 3]), (int, float))
    assert isinstance(mod.discount_amount(10, 10), (int, float))
    assert isinstance(mod.tax_amount(10, 10), (int, float))
    assert isinstance(mod.final_total([1, 2, 3], 10, 10), (int, float))