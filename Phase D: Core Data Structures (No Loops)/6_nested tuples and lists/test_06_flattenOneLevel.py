import importlib.util
import io
import os
import sys
import ast
import pytest

MODULE_NAME = "06_flattenOneLevel"
FILE_NAME = "06_flattenOneLevel.py"


def load_module_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return module, buf.getvalue()


def test_prints_expected_list():
    _, out = load_module_capture_stdout()
    expected = "[1, 2, 3, 4, 5]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_flat_is_list_with_expected_contents():
    module, _ = load_module_capture_stdout()
    assert isinstance(module.flat, list), f"expected={list} actual={type(module.flat)}"
    expected = [1, 2, 3, 4, 5]
    assert module.flat == expected, f"expected={expected!r} actual={module.flat!r}"


def test_flat_is_new_list_not_alias_of_nested_sublist():
    module, _ = load_module_capture_stdout()
    assert module.flat is not module.nested, f"expected={True!r} actual={(module.flat is not module.nested)!r}"
    for sub in module.nested:
        assert module.flat is not sub, f"expected={True!r} actual={(module.flat is not sub)!r}"


def test_flat_elements_are_ints_in_order():
    module, _ = load_module_capture_stdout()
    expected_types = [int, int, int, int, int]
    actual_types = [type(x) for x in module.flat]
    assert actual_types == expected_types, f"expected={expected_types!r} actual={actual_types!r}"


def test_no_hardcoded_literal_flat_list_in_source():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src, filename=FILE_NAME)
    banned = [1, 2, 3, 4, 5]

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "flat":
                    if isinstance(node.value, ast.List):
                        try:
                            val = ast.literal_eval(node.value)
                        except Exception:
                            val = None
                        assert val != banned, f"expected={True!r} actual={(val == banned)!r}"