import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILE = "03_enumerateBuildListOfTuples.py"


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location("student_mod_03", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _expected_indexed():
    letters = ["A", "B", "C", "D"]
    return list(enumerate(letters))


def test_module_runs_without_error():
    mod, out = _run_module_capture_stdout()
    assert hasattr(mod, "letters")
    assert hasattr(mod, "indexed")


def test_indexed_value_correct():
    mod, _ = _run_module_capture_stdout()
    expected = _expected_indexed()
    actual = getattr(mod, "indexed")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_indexed():
    mod, out = _run_module_capture_stdout()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) >= 1, f"expected>=1 actual={len(lines)}"
    last = lines[-1]
    try:
        printed = ast.literal_eval(last)
    except Exception:
        printed = last
    expected = getattr(mod, "indexed")
    assert printed == expected, f"expected={expected} actual={printed}"


def test_uses_enumerate_in_source():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    has_enum = any(isinstance(c.func, ast.Name) and c.func.id == "enumerate" for c in calls)
    assert has_enum is True, f"expected={True} actual={has_enum}"


def test_indexed_is_list_of_tuples_of_int_str():
    mod, _ = _run_module_capture_stdout()
    actual = getattr(mod, "indexed")
    expected = _expected_indexed()
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    assert len(actual) == len(expected), f"expected={len(expected)} actual={len(actual)}"
    for item in actual:
        assert isinstance(item, tuple), f"expected={tuple} actual={type(item)}"
        assert len(item) == 2, f"expected={2} actual={len(item)}"
        i, v = item
        assert isinstance(i, int), f"expected={int} actual={type(i)}"
        assert isinstance(v, str), f"expected={str} actual={type(v)}"