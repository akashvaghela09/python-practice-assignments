import ast
import importlib.util
import io
import os
import sys

import pytest


FILE_NAME = "11_convertListOfTuplesToLists.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("student_mod_11", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec = importlib.util.spec_from_file_location("student_run_11", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_expected_output_exactly():
    out = _run_script_capture_stdout()
    expected = "[[1, 2], [3, 4], [5, 6]]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_converted_value_and_types():
    mod = _load_module()
    expected = [[1, 2], [3, 4], [5, 6]]
    actual = getattr(mod, "converted", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, list), f"expected={list!r} actual={type(actual)!r}"
    assert all(isinstance(x, list) for x in actual), f"expected={True!r} actual={all(isinstance(x, list) for x in actual)!r}"
    assert all(not isinstance(x, tuple) for x in actual), f"expected={True!r} actual={all(not isinstance(x, tuple) for x in actual)!r}"


def test_source_does_not_leave_converted_as_none():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=FILE_NAME)

    assigned_none = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "converted":
                    val = node.value
                    if isinstance(val, ast.Constant) and val.value is None:
                        assigned_none = True

    assert assigned_none is False, f"expected={False!r} actual={assigned_none!r}"