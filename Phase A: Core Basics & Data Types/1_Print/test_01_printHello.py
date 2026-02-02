import importlib.util
import io
import os
import sys
import pytest

FILE_NAME = "01_printHello.py"


def _run_script_capture_stdout(path):
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        spec = importlib.util.spec_from_file_location("student_module_01_printHello", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_file_exists():
    assert os.path.exists(FILE_NAME)


def test_prints_exact_output():
    out = _run_script_capture_stdout(FILE_NAME)
    expected = "Hello, world!\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output_lines():
    out = _run_script_capture_stdout(FILE_NAME)
    expected_lines = ["Hello, world!"]
    actual_lines = out.splitlines()
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"