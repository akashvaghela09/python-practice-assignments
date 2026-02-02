import importlib
import io
import contextlib
import ast
import os
import sys
import pytest

MODULE_NAME = "08_nestedTuplesAndAccess"


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if MODULE_NAME in sys.modules:
            importlib.reload(sys.modules[MODULE_NAME])
        else:
            importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def _parse_module_source():
    module = importlib.import_module(MODULE_NAME)
    path = module.__file__
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _get_assigned_names(tree):
    assigned = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    assigned.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assigned.add(node.target.id)
    return assigned


def _get_literal_person_value(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "person":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "person":
            try:
                return ast.literal_eval(node.value)
            except Exception:
                return None
    return None


def test_stdout_has_two_lines_expected_values():
    out = _run_module_capture_stdout()
    lines = out.splitlines()
    assert len(lines) == 2, f"expected=2 actual={len(lines)}"
    assert lines[0] == "Ada", f"expected={'Ada'} actual={lines[0]}"
    assert lines[1] == "London", f"expected={'London'} actual={lines[1]}"


def test_variables_name_and_city_assigned():
    src = _parse_module_source()
    tree = ast.parse(src)
    assigned = _get_assigned_names(tree)
    assert "name" in assigned, f"expected={'name in assigned'} actual={assigned}"
    assert "city" in assigned, f"expected={'city in assigned'} actual={assigned}"


def test_person_literal_structure_and_values():
    src = _parse_module_source()
    tree = ast.parse(src)
    person_val = _get_literal_person_value(tree)
    assert person_val is not None, f"expected={'literal person'} actual={person_val}"
    assert isinstance(person_val, tuple), f"expected={tuple} actual={type(person_val)}"
    assert len(person_val) == 2, f"expected=2 actual={len(person_val)}"
    assert person_val[0] == "Ada", f"expected={'Ada'} actual={person_val[0]}"
    assert isinstance(person_val[1], tuple), f"expected={tuple} actual={type(person_val[1])}"
    assert len(person_val[1]) == 2, f"expected=2 actual={len(person_val[1])}"
    assert person_val[1][1] == "London", f"expected={'London'} actual={person_val[1][1]}"


def test_import_does_not_raise():
    try:
        _run_module_capture_stdout()
    except Exception as e:
        pytest.fail(f"expected={'no exception'} actual={type(e).__name__}")