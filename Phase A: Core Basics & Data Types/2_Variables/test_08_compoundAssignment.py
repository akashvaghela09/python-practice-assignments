import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

MODULE_FILENAME = "08_compoundAssignment.py"


def _run_module_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("compound_assignment_mod", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_output_exact():
    _, out = _run_module_capture_stdout()
    expected = "result=18\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_value_final_state():
    module, _ = _run_module_capture_stdout()
    expected = 18
    actual = getattr(module, "value", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_single_line_output():
    _, out = _run_module_capture_stdout()
    expected_lines = 1
    actual_lines = len(out.splitlines())
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"