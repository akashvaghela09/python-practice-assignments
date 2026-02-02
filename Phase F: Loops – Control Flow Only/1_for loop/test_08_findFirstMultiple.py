import importlib
import io
import sys
import types
import pytest

MODULE_NAME = "08_findFirstMultiple"


def _run_module_capture_stdout():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(MODULE_NAME)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_expected_value():
    out = _run_module_capture_stdout()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected one line, got {len(lines)}"
    assert lines[0] == "21", f"expected 21, got {lines[0]}"


def test_no_placeholder_blanks_left():
    src = importlib.util.find_spec(MODULE_NAME).loader.get_source(MODULE_NAME)
    assert "____" not in src, f"expected no placeholders, got {'____'}"


def test_uses_for_loop():
    src = importlib.util.find_spec(MODULE_NAME).loader.get_source(MODULE_NAME)
    assert "for " in src, f"expected for-loop, got source without for-loop"


def test_uses_break_statement():
    src = importlib.util.find_spec(MODULE_NAME).loader.get_source(MODULE_NAME)
    assert "break" in src, f"expected break usage, got source without break"


def test_found_is_first_multiple_of_7_not_later_one():
    out = _run_module_capture_stdout()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert lines and lines[0] != "28", f"expected not 28, got {lines[0] if lines else lines}"