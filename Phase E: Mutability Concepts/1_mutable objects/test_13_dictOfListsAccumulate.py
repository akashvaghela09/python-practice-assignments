import importlib.util
import os
import subprocess
import sys
import ast
import pytest

MODULE_FILE = "13_dictOfListsAccumulate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("dict_accumulate_mod", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script():
    proc = subprocess.run(
        [sys.executable, MODULE_FILE],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(MODULE_FILE)) or None,
    )
    return proc


def test_add_to_group_creates_and_appends_in_order():
    mod = load_module()
    groups = {}
    mod.add_to_group(groups, "fruit", "apple")
    mod.add_to_group(groups, "fruit", "banana")
    mod.add_to_group(groups, "veg", "carrot")
    expected = {"fruit": ["apple", "banana"], "veg": ["carrot"]}
    assert groups == expected, f"expected={expected!r} actual={groups!r}"


def test_add_to_group_mutates_existing_dict_object():
    mod = load_module()
    groups = {}
    before_id = id(groups)
    ret = mod.add_to_group(groups, "x", "y")
    after_id = id(groups)
    assert after_id == before_id, f"expected={before_id!r} actual={after_id!r}"
    assert ret is None, f"expected={None!r} actual={ret!r}"


def test_add_to_group_accumulates_without_overwriting_list():
    mod = load_module()
    groups = {"fruit": ["apple"]}
    orig_list_id = id(groups["fruit"])
    mod.add_to_group(groups, "fruit", "banana")
    new_list_id = id(groups["fruit"])
    assert new_list_id == orig_list_id, f"expected={orig_list_id!r} actual={new_list_id!r}"
    expected = {"fruit": ["apple", "banana"]}
    assert groups == expected, f"expected={expected!r} actual={groups!r}"


def test_main_prints_exact_expected_dict_repr():
    proc = run_script()
    assert proc.returncode == 0, f"expected={0!r} actual={proc.returncode!r}"
    out = proc.stdout.strip()
    expected = "{'fruit': ['apple', 'banana'], 'veg': ['carrot']}"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_output_is_valid_python_literal_and_matches():
    proc = run_script()
    assert proc.returncode == 0, f"expected={0!r} actual={proc.returncode!r}"
    out = proc.stdout.strip()
    parsed = ast.literal_eval(out)
    expected = {"fruit": ["apple", "banana"], "veg": ["carrot"]}
    assert parsed == expected, f"expected={expected!r} actual={parsed!r}"


def test_no_unexpected_stderr_output():
    proc = run_script()
    assert proc.returncode == 0, f"expected={0!r} actual={proc.returncode!r}"
    err = proc.stderr.strip()
    expected = ""
    assert err == expected, f"expected={expected!r} actual={err!r}"