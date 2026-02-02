import importlib.util
import io
import os
import sys


def _run_script_capture_output(script_path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("module_under_test", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_output_matches_expected():
    script_path = os.path.join(os.path.dirname(__file__), "03_printWithQuotes.py")
    actual = _run_script_capture_output(script_path)
    expected = 'She said, "Python is fun!"\n'
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_extra_whitespace_or_lines():
    script_path = os.path.join(os.path.dirname(__file__), "03_printWithQuotes.py")
    actual = _run_script_capture_output(script_path)
    expected = 'She said, "Python is fun!"\n'
    assert actual == expected, f"expected={expected!r} actual={actual!r}"