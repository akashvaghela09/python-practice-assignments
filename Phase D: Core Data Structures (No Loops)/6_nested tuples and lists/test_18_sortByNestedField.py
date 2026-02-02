import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

import pytest


MODULE_FILENAME = "18_sortByNestedField.py"
MODULE_NAME = "m18_sortByNestedField"


def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_file_capture_stdout(path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        load_module_from_path(path)
    return buf.getvalue()


def test_prints_expected_sorted_records(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    test_path = tmp_path / MODULE_FILENAME
    test_path.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    out = run_file_capture_stdout(str(test_path)).strip()
    expected = "[('Bea', (19, 92)), ('Cal', (21, 88)), ('Ada', (20, 75))]"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_sorted_records_variable_is_correct(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    test_path = tmp_path / MODULE_FILENAME
    test_path.write_text(open(src_path, "r", encoding="utf-8").read(), encoding="utf-8")

    module = load_module_from_path(str(test_path))

    expected = [('Bea', (19, 92)), ('Cal', (21, 88)), ('Ada', (20, 75))]
    actual = getattr(module, "sorted_records", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sorted_records_is_new_list_and_not_mutating_records(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    code = open(src_path, "r", encoding="utf-8").read()
    test_path = tmp_path / MODULE_FILENAME
    test_path.write_text(code, encoding="utf-8")

    module = load_module_from_path(str(test_path))

    original = [("Ada", (20, 75)), ("Bea", (19, 92)), ("Cal", (21, 88))]
    actual_records = getattr(module, "records", None)
    assert actual_records == original, f"expected={original!r} actual={actual_records!r}"

    sorted_records = getattr(module, "sorted_records", None)
    assert isinstance(sorted_records, list), f"expected={list!r} actual={type(sorted_records)!r}"
    assert sorted_records is not actual_records, f"expected={'different object'!r} actual={'same object'!r}"


def test_uses_score_descending_key_hint(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    code = open(src_path, "r", encoding="utf-8").read()
    test_path = tmp_path / MODULE_FILENAME
    test_path.write_text(code, encoding="utf-8")

    tree = ast.parse(code)

    has_sorted_or_sort = False
    has_reverse_true = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "sorted":
                has_sorted_or_sort = True
                for kw in node.keywords:
                    if kw.arg == "reverse" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        has_reverse_true = True
            if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                has_sorted_or_sort = True
                for kw in node.keywords:
                    if kw.arg == "reverse" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        has_reverse_true = True

    assert has_sorted_or_sort, f"expected={'sorted/sort used'!r} actual={'not found'!r}"
    assert has_reverse_true, f"expected={'reverse=True'!r} actual={'not found'!r}"