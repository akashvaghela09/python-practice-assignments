import importlib.util
import os
import sys
import re

MODULE_FILE = "10_safeDefaultArgs.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    spec = importlib.util.spec_from_file_location("safe_default_args_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_prints_expected_output(capsys):
    load_module()
    out = capsys.readouterr().out
    expected = "()\n(1,)\n()\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_add_item_returns_new_tuple_and_is_pure():
    mod = load_module()

    base = (9,)
    res = mod.add_item(1, base)
    assert isinstance(res, tuple), f"expected={tuple!r} actual={type(res)!r}"
    assert res == (9, 1), f"expected={(9, 1)!r} actual={res!r}"
    assert base == (9,), f"expected={(9,)!r} actual={base!r}"
    assert res is not base, f"expected={'different objects'!r} actual={'same object'!r}"

    res2 = mod.add_item(None)
    assert res2 == (None,), f"expected={(None,)!r} actual={res2!r}"

    res3 = mod.add_item(None)
    assert res3 == (None,), f"expected={(None,)!r} actual={res3!r}"


def test_default_items_not_mutated_across_calls():
    mod = load_module()

    sig_defaults = mod.add_item.__defaults__
    assert isinstance(sig_defaults, tuple), f"expected={tuple!r} actual={type(sig_defaults)!r}"
    assert len(sig_defaults) == 1, f"expected={1!r} actual={len(sig_defaults)!r}"
    default_items = sig_defaults[0]
    assert default_items == (), f"expected={().!r} actual={default_items!r}"

    mod.add_item("x")
    mod.add_item("y")
    assert mod.add_item.__defaults__[0] == (), f"expected={().!r} actual={mod.add_item.__defaults__[0]!r}"


def test_no_list_default_used_in_signature():
    mod = load_module()
    src = inspect.getsource(mod.add_item)
    assert "items=[]" not in src.replace(" ", ""), f"expected={'no list default'!r} actual={'list default found'!r}"


def test_module_has_no_pass_in_add_item_body():
    mod = load_module()
    import inspect

    src = inspect.getsource(mod.add_item)
    has_pass = re.search(r"^\s*pass\s*$", src, re.MULTILINE) is not None
    assert not has_pass, f"expected={'implemented'!r} actual={'contains pass'!r}"