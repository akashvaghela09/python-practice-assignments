import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

MODULE_NAME = "04_listFromVariables"
FILE_NAME = "04_listFromVariables.py"


def load_module():
    spec = importlib.util.spec_from_file_location(MODULE_NAME, os.path.join(os.getcwd(), FILE_NAME))
    module = importlib.util.module_from_spec(spec)
    return spec, module


def test_file_parses():
    path = os.path.join(os.getcwd(), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    ast.parse(src)


def test_coords_is_list_in_correct_order_and_values():
    spec, module = load_module()
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)

    assert hasattr(module, "x")
    assert hasattr(module, "y")
    assert hasattr(module, "z")
    assert hasattr(module, "coords")

    expected = [module.x, module.y, module.z]
    actual = module.coords
    assert isinstance(actual, list), f"expected={list!r} actual={type(actual)!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_coords_once_and_matches_value():
    spec, module = load_module()
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)

    out_lines = [line.rstrip("\n") for line in buf.getvalue().splitlines() if line.strip() != ""]
    assert len(out_lines) == 1, f"expected={1!r} actual={len(out_lines)!r}"

    expected_str = str(module.coords)
    actual_str = out_lines[0]
    assert actual_str == expected_str, f"expected={expected_str!r} actual={actual_str!r}"