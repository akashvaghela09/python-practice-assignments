import importlib
import contextlib
import io
import sys
import pytest

MODULE_NAME = "02_countDownBasics"

def run_module():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()

def test_outputs_countdown_lines():
    out = run_module()
    expected_lines = ["5", "4", "3", "2", "1"]
    actual_lines = [line.rstrip("\n") for line in out.splitlines()]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"

def test_outputs_exactly_five_lines():
    out = run_module()
    actual_lines = [line.rstrip("\n") for line in out.splitlines()]
    expected_count = 5
    actual_count = len(actual_lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"

def test_no_extra_whitespace_per_line():
    out = run_module()
    actual_lines = out.splitlines()
    expected_lines = ["5", "4", "3", "2", "1"]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"