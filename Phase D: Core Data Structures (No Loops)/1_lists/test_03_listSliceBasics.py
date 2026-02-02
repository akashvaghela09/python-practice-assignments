import ast
import importlib.util
import os
import sys
import types
import pytest


ASSIGNMENT_FILE = "03_listSliceBasics.py"


def _load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _get_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_file_exists():
    assert os.path.exists(ASSIGNMENT_FILE), f"expected exists=True actual exists={os.path.exists(ASSIGNMENT_FILE)}"


def test_source_is_valid_python():
    src = _get_source(ASSIGNMENT_FILE)
    try:
        ast.parse(src)
        ok = True
    except SyntaxError:
        ok = False
    assert ok, f"expected syntax_ok=True actual syntax_ok={ok}"


def test_middle_is_correct_sublist_and_printed(capsys):
    mod = _load_module(ASSIGNMENT_FILE)
    captured = capsys.readouterr()
    assert hasattr(mod, "nums"), "expected has_nums=True actual has_nums=False"
    assert hasattr(mod, "middle"), "expected has_middle=True actual has_middle=False"
    expected = [20, 30, 40]
    actual = getattr(mod, "middle")
    assert actual == expected, f"expected middle={expected!r} actual middle={actual!r}"
    out = captured.out.strip().splitlines()[-1].strip() if captured.out.strip() else ""
    assert out == repr(expected), f"expected printed={repr(expected)!r} actual printed={out!r}"


def test_middle_is_slice_not_literal():
    src = _get_source(ASSIGNMENT_FILE)
    tree = ast.parse(src)

    middle_value = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "middle":
                    middle_value = node.value
                    break

    assert middle_value is not None, "expected middle_assigned=True actual middle_assigned=False"
    is_subscript = isinstance(middle_value, ast.Subscript)
    is_list_literal = isinstance(middle_value, ast.List)
    assert is_subscript and not is_list_literal, f"expected uses_slice=True actual uses_slice={is_subscript and not is_list_literal}"


def test_nums_unchanged():
    mod = _load_module(ASSIGNMENT_FILE)
    expected = [10, 20, 30, 40, 50]
    actual = getattr(mod, "nums", None)
    assert actual == expected, f"expected nums={expected!r} actual nums={actual!r}"