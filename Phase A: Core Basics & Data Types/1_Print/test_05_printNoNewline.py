import importlib.util
import io
import os
import sys


def run_script_capture_stdout(script_path):
    spec = importlib.util.spec_from_file_location("assignment_mod", script_path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_output_exact():
    script_path = os.path.join(os.path.dirname(__file__), "05_printNoNewline.py")
    out = run_script_capture_stdout(script_path)
    expected = "Hello there\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_whitespace_or_lines():
    script_path = os.path.join(os.path.dirname(__file__), "05_printNoNewline.py")
    out = run_script_capture_stdout(script_path)
    expected = "Hello there\n"
    assert out.strip("\n") == expected.strip("\n"), f"expected={expected.strip(chr(10))!r} actual={out.strip(chr(10))!r}"
    assert out.count("\n") == expected.count("\n"), f"expected={expected.count(chr(10))!r} actual={out.count(chr(10))!r}"
    assert "  " not in out, f"expected={'no double spaces'!r} actual={out!r}"