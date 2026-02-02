import importlib.util
import io
import os
import sys


def run_script_capture_stdout(path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("student_module_05", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_prints_only_non_empty_trimmed_tokens():
    path = os.path.join(os.path.dirname(__file__), "05_skipEmptyTokens.py")
    out = run_script_capture_stdout(path)
    expected_lines = ["apple", "banana", "pear"]
    actual_lines = out.splitlines()

    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_no_blank_lines_or_whitespace_only_lines():
    path = os.path.join(os.path.dirname(__file__), "05_skipEmptyTokens.py")
    out = run_script_capture_stdout(path)
    lines = out.splitlines()

    expected = []
    actual = [ln for ln in lines if ln.strip() == ""]
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_exact_line_count():
    path = os.path.join(os.path.dirname(__file__), "05_skipEmptyTokens.py")
    out = run_script_capture_stdout(path)
    expected = 3
    actual = len(out.splitlines())
    assert actual == expected, f"expected={expected!r} actual={actual!r}"