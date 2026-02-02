import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILENAME = "05_collectSquares.py"


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("collectSquares_mod", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def test_no_placeholders_left():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "____" not in src


def test_prints_expected_list():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    _, out = _run_module_capture_stdout(path)
    got = _parse_last_list_from_stdout(out)
    expected = [1, 4, 9, 16]
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_variables_present_and_correct():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    mod, _ = _run_module_capture_stdout(path)
    assert hasattr(mod, "nums")
    assert hasattr(mod, "squares")
    expected_nums = [1, 2, 3, 4]
    expected_squares = [1, 4, 9, 16]
    assert mod.nums == expected_nums, f"expected={expected_nums!r} actual={getattr(mod, 'nums', None)!r}"
    assert mod.squares == expected_squares, f"expected={expected_squares!r} actual={getattr(mod, 'squares', None)!r}"


def test_squares_is_new_list_not_alias_of_nums():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    mod, _ = _run_module_capture_stdout(path)
    assert isinstance(mod.nums, list)
    assert isinstance(mod.squares, list)
    assert mod.squares is not mod.nums, f"expected={'different_objects'} actual={'same_object' if mod.squares is mod.nums else 'different_objects'}"