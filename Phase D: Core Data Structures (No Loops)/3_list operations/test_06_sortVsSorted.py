import importlib.util
import io
import os
import sys
import ast
import pytest


FILE_NAME = "06_sortVsSorted.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("mod_06_sortVsSorted", path)
    module = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(module)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return module, output, path


def test_module_executes_without_syntax_error():
    _, _, path = load_module()
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    ast.parse(src)


def test_print_output_matches_expected_lines():
    module, output, _ = load_module()
    expected = "original=[3, 1, 2]\nsorted_copy=[1, 2, 3]\nafter_sort=[1, 2, 3]\n"
    assert output == expected, f"expected={expected!r} actual={output!r}"
    assert hasattr(module, "values")
    assert hasattr(module, "sorted_copy")


def test_sorted_copy_is_new_list_and_values_sorted_in_place_after():
    module, _, _ = load_module()
    assert isinstance(module.values, list)
    assert isinstance(module.sorted_copy, list)
    assert module.values == [1, 2, 3], f"expected={[1,2,3]!r} actual={module.values!r}"
    assert module.sorted_copy == [1, 2, 3], f"expected={[1,2,3]!r} actual={module.sorted_copy!r}"
    assert module.sorted_copy is not module.values, f"expected={'different_objects'!r} actual={'same_object'!r}"


def test_sorted_copy_does_not_alias_values_or_change_with_it():
    module, _, _ = load_module()
    before = list(module.sorted_copy)
    module.values.append(99)
    after = list(module.sorted_copy)
    assert after == before, f"expected={before!r} actual={after!r}"