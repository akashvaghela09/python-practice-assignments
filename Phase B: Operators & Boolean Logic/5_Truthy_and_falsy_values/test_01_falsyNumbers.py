import importlib.util
import io
import os
import contextlib
import pytest

MODULE_FILE = "01_falsyNumbers.py"


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location("mod_01_falsyNumbers", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return buf.getvalue()


def test_prints_exactly_falsy():
    out = _run_module_capture_stdout()
    expected = "FALSY\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_one_line_only():
    out = _run_module_capture_stdout()
    lines = out.splitlines(True)
    expected_count = 1
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_no_extra_whitespace_or_text():
    out = _run_module_capture_stdout()
    expected = "FALSY"
    actual = out.rstrip("\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_source_contains_no_placeholder_marker():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    expected = False
    actual = "__" in src
    assert actual == expected, f"expected={expected!r} actual={actual!r}"