import importlib
import sys


def load_module_fresh(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


def test_output_exact(capsys):
    load_module_fresh("07_dict_membership_keys_vs_values")
    out = capsys.readouterr().out
    expected = "key_exists\nvalue_missing\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_does_not_print_value_exists(capsys):
    load_module_fresh("07_dict_membership_keys_vs_values")
    out = capsys.readouterr().out
    expected_contains = "value_exists"
    assert expected_contains not in out, f"expected_not_in={expected_contains!r} actual={out!r}"


def test_prices_dict_integrity():
    mod = load_module_fresh("07_dict_membership_keys_vs_values")
    assert isinstance(mod.prices, dict), f"expected={dict!r} actual={type(mod.prices)!r}"
    expected = {"apple": 1.25, "banana": 0.75}
    assert mod.prices == expected, f"expected={expected!r} actual={mod.prices!r}"