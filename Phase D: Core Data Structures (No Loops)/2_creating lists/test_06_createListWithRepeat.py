import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILENAME = "06_createListWithRepeat.py"


def load_module():
    module_name = "m06_createListWithRepeat"
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(os.getcwd(), MODULE_FILENAME))
    module = importlib.util.module_from_spec(spec)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        spec.loader.exec_module(module)
    return module, captured.getvalue()


def test_script_runs_without_syntax_error():
    try:
        load_module()
    except SyntaxError as e:
        pytest.fail(f"expected no SyntaxError, got {type(e).__name__}: {e}")


def test_zeros_exists_and_is_list_of_five_zeros():
    try:
        module, _ = load_module()
    except Exception as e:
        pytest.fail(f"expected module import to succeed, got {type(e).__name__}: {e}")

    assert hasattr(module, "zeros"), "expected zeros to exist, got missing"
    zeros = getattr(module, "zeros")
    assert isinstance(zeros, list), f"expected list, got {type(zeros).__name__}"
    assert len(zeros) == 5, f"expected length 5, got {len(zeros)}"
    assert all(x == 0 for x in zeros), f"expected all elements 0, got {zeros}"


def test_printed_output_matches_list_repr():
    try:
        module, out = load_module()
    except Exception as e:
        pytest.fail(f"expected module import to succeed, got {type(e).__name__}: {e}")

    zeros = getattr(module, "zeros", None)
    expected = f"{zeros}\n"
    assert out == expected, f"expected {expected!r}, got {out!r}"


def test_uses_repetition_operator_in_assignment():
    src = open(MODULE_FILENAME, "r", encoding="utf-8").read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        pytest.fail(f"expected valid syntax, got {type(e).__name__}: {e}")

    assigns = [
        n for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "zeros" for t in n.targets)
    ]
    assert assigns, "expected assignment to zeros, got none"

    value = assigns[0].value
    assert isinstance(value, ast.BinOp) and isinstance(value.op, ast.Mult), f"expected repetition using *, got {type(value).__name__}"
    left_is_list = isinstance(value.left, ast.List)
    right_is_list = isinstance(value.right, ast.List)
    assert left_is_list or right_is_list, f"expected one side list literal, got left={type(value.left).__name__}, right={type(value.right).__name__}"