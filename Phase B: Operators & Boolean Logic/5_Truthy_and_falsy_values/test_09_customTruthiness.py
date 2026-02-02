import importlib.util
import os
import sys
import pytest


MODULE_FILENAME = "09_customTruthiness.py"


def load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    if not os.path.exists(src):
        src = MODULE_FILENAME
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod_09", str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_import_has_no_placeholder_underscores(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    if not os.path.exists(src):
        src = MODULE_FILENAME
    code = open(src, "r", encoding="utf-8").read()
    assert "__\n" not in code and "__\r\n" not in code


def test_printed_output_exact(tmp_path, capsys):
    load_module(tmp_path)
    out = capsys.readouterr().out
    actual = out.splitlines()
    expected = ["EMPTY", "NOT EMPTY"]
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_bool_behavior(tmp_path):
    mod = load_module(tmp_path)
    Cart = mod.Cart

    c_empty = Cart([])
    c_one = Cart(["x"])
    c_many = Cart([1, 2, 3])

    assert bool(c_empty) is False, f"expected={False!r} actual={bool(c_empty)!r}"
    assert bool(c_one) is True, f"expected={True!r} actual={bool(c_one)!r}"
    assert bool(c_many) is True, f"expected={True!r} actual={bool(c_many)!r}"


def test_items_mutation_affects_truthiness(tmp_path):
    mod = load_module(tmp_path)
    Cart = mod.Cart

    c = Cart([])
    assert bool(c) is False, f"expected={False!r} actual={bool(c)!r}"
    c.items.append("a")
    assert bool(c) is True, f"expected={True!r} actual={bool(c)!r}"
    c.items.clear()
    assert bool(c) is False, f"expected={False!r} actual={bool(c)!r}"


def test_bool_returns_bool_type(tmp_path):
    mod = load_module(tmp_path)
    Cart = mod.Cart
    c = Cart(["a"])
    result = c.__bool__()
    assert type(result) is bool, f"expected={bool!r} actual={type(result)!r}"