import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_mod_10_stripWhitespace", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return buf.getvalue(), module


def test_output_strips_whitespace():
    out, _ = _run_module_capture_stdout("10_stripWhitespace.py")
    expected = "[Python]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_clean_variable_value():
    out, mod = _run_module_capture_stdout("10_stripWhitespace.py")
    expected_clean = "Python"
    actual_clean = getattr(mod, "clean", None)
    assert actual_clean == expected_clean, f"expected={expected_clean!r} actual={actual_clean!r}"


def test_raw_unchanged_and_is_string():
    _, mod = _run_module_capture_stdout("10_stripWhitespace.py")
    assert isinstance(getattr(mod, "raw", None), str)
    expected_raw = "   Python   "
    actual_raw = getattr(mod, "raw", None)
    assert actual_raw == expected_raw, f"expected={expected_raw!r} actual={actual_raw!r}"