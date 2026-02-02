import ast
import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILE = "01_enumerateBasics_printIndexAndItem.py"


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_module_capture_stdout(path):
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        mod = load_module_from_path(path, "student_module_capture")
    finally:
        sys.stdout = old
    return buf.getvalue(), mod


def test_file_exists():
    assert os.path.exists(MODULE_FILE)


def test_no_placeholders_left():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    assert "___" not in src


def test_uses_enumerate():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "enumerate":
            found = True
            break
    assert found


def test_prints_expected_lines():
    out, _ = run_module_capture_stdout(MODULE_FILE)
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    expected = [f"{i} {fruit}" for i, fruit in enumerate(["apple", "banana", "cherry"])]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_only_expected_number_of_nonempty_lines():
    out, _ = run_module_capture_stdout(MODULE_FILE)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_count = len(["apple", "banana", "cherry"])
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_fruits_list_unchanged():
    _, mod = run_module_capture_stdout(MODULE_FILE)
    assert hasattr(mod, "fruits")
    expected = ["apple", "banana", "cherry"]
    actual = getattr(mod, "fruits")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"