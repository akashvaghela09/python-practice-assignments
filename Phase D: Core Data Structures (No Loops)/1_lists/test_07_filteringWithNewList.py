import importlib.util
import os
import sys
import types
import ast
import pytest


ASSIGNMENT_FILE = "07_filteringWithNewList.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), ASSIGNMENT_FILE)
    spec = importlib.util.spec_from_file_location("student_mod_07", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_source():
    path = os.path.join(os.path.dirname(__file__), ASSIGNMENT_FILE)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_has_evens_variable_and_is_list():
    mod = _load_module()
    assert hasattr(mod, "evens"), "expected evens to exist, actual missing"
    assert isinstance(mod.evens, list), f"expected list, actual {type(mod.evens).__name__}"


def test_evens_contains_only_even_numbers_and_matches_expected():
    mod = _load_module()
    expected = [2, 4, 6]
    actual = mod.evens
    assert actual == expected, f"expected {expected}, actual {actual}"
    assert all(isinstance(x, int) and x % 2 == 0 for x in actual), f"expected all even ints, actual {actual}"


def test_original_nums_not_modified():
    mod = _load_module()
    expected_nums = [1, 2, 3, 4, 5, 6]
    actual_nums = getattr(mod, "nums", None)
    assert actual_nums == expected_nums, f"expected {expected_nums}, actual {actual_nums}"


def test_evens_is_new_list_not_alias_of_nums():
    mod = _load_module()
    assert mod.evens is not mod.nums, f"expected different objects, actual same id {id(mod.evens)}"


def test_output_prints_evens_line(capsys):
    _load_module()
    captured = capsys.readouterr()
    expected_line = "evens: [2, 4, 6]"
    actual_out = captured.out.strip().splitlines()
    assert expected_line in actual_out, f"expected {expected_line!r}, actual {captured.out!r}"


def test_does_not_use_incorrect_variable_name_in_final_code():
    src = _read_source()
    assert "evans" not in src, f"expected no 'evans' in source, actual found in {ASSIGNMENT_FILE}"


def test_uses_loop_and_append_or_comprehension():
    src = _read_source()
    tree = ast.parse(src)

    has_for = any(isinstance(n, ast.For) for n in ast.walk(tree))
    has_append_call = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "append":
                has_append_call = True
                break

    has_listcomp = any(isinstance(n, ast.ListComp) for n in ast.walk(tree))

    assert (has_listcomp or (has_for and has_append_call)), f"expected loop+append or list comprehension, actual for={has_for} append={has_append_call} listcomp={has_listcomp}"