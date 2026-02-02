import importlib
import io
import contextlib
import re

def run_module_capture():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module("06_unaryMinusVsExponent")
    return buf.getvalue()

def test_prints_negative_nine_exactly():
    out = run_module_capture()
    actual = out
    expected = "-9\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

def test_prints_single_integer_line_only():
    out = run_module_capture()
    actual = out
    expected_pattern = r"^-?\d+\n$"
    assert re.match(expected_pattern, actual) is not None, f"expected={expected_pattern!r} actual={actual!r}"