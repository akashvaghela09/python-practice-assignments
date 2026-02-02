import importlib.util
import io
import os
import contextlib
import pytest


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_03", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return buf.getvalue()


def test_script_runs_without_syntax_error():
    path = os.path.join(os.path.dirname(__file__), "03_boolFromValues.py")
    try:
        _run_script_capture_stdout(path)
    except SyntaxError as e:
        pytest.fail(f"expected=no_syntax_error actual=SyntaxError:{e.msg}")


def test_output_exact_three_lines():
    path = os.path.join(os.path.dirname(__file__), "03_boolFromValues.py")
    out = _run_script_capture_stdout(path)

    expected = "False\nFalse\nTrue\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_output_has_no_extra_whitespace_or_lines():
    path = os.path.join(os.path.dirname(__file__), "03_boolFromValues.py")
    out = _run_script_capture_stdout(path)
    lines = out.splitlines()
    expected_lines = ["False", "False", "True"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"