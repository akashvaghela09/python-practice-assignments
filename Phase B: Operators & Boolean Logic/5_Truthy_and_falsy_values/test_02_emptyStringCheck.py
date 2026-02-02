import importlib.util
import os
import sys
from contextlib import redirect_stdout
from io import StringIO


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture_output(path):
    buf = StringIO()
    with redirect_stdout(buf):
        load_module_from_path("student_module_02_emptyStringCheck", path)
    return buf.getvalue()


def test_prints_empty_only():
    path = os.path.join(os.path.dirname(__file__), "02_emptyStringCheck.py")
    out = run_script_capture_output(path)
    expected = "EMPTY\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_nonempty_printed():
    path = os.path.join(os.path.dirname(__file__), "02_emptyStringCheck.py")
    out = run_script_capture_output(path)
    expected = False
    actual = "NONEMPTY" in out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_exact_single_line():
    path = os.path.join(os.path.dirname(__file__), "02_emptyStringCheck.py")
    out = run_script_capture_output(path)
    expected = 1
    actual = len([line for line in out.splitlines() if line.strip() != ""])
    assert actual == expected, f"expected={expected!r} actual={actual!r}"