import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location(module_filename.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_prints_numbers_1_to_5_exact():
    out = _run_module_capture_stdout("01_printNumbers.py")
    expected = "1\n2\n3\n4\n5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_five_lines_no_extra_whitespace():
    out = _run_module_capture_stdout("01_printNumbers.py")
    lines = out.splitlines()
    expected_lines = ["1", "2", "3", "4", "5"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"