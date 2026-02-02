import importlib
import io
import sys
import re
import pytest


def run_module_capture(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(module_name)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_exact_total_with_two_decimals():
    out = run_module_capture("07_printFormattedNumbers").replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln for ln in out.split("\n") if ln.strip() != ""]
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"
    expected = "Total: 19.90"
    assert lines[0] == expected, f"expected={expected!r} actual={lines[0]!r}"


def test_two_decimal_places_present():
    out = run_module_capture("07_printFormattedNumbers").replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln for ln in out.split("\n") if ln.strip() != ""]
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"
    m = re.fullmatch(r"Total:\s+([0-9]+)\.([0-9]{2})", lines[0])
    assert m is not None, f"expected={'match'!r} actual={lines[0]!r}"


def test_does_not_print_extra_text():
    out = run_module_capture("07_printFormattedNumbers").replace("\r\n", "\n").replace("\r", "\n")
    stripped = out.strip("\n")
    expected = "Total: 19.90"
    assert stripped == expected, f"expected={expected!r} actual={stripped!r}"