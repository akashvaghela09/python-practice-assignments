import importlib.util
import io
import os
import re
import sys
import types
import pytest

MODULE_FILE = "10_extractDigits.py"


def _run_module_capture():
    spec = importlib.util.spec_from_file_location("student_mod_10", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout
    return mod, buf.getvalue()


def _parse_output(out):
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    return lines


def test_runs_without_error_and_prints_two_lines():
    mod, out = _run_module_capture()
    lines = _parse_output(out)
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"


def test_output_format_labels_and_integers():
    mod, out = _run_module_capture()
    lines = _parse_output(out)
    assert re.fullmatch(r"tens=-?\d+", lines[0]) is not None, f"expected={r'tens=<int>'!r} actual={lines[0]!r}"
    assert re.fullmatch(r"ones=-?\d+", lines[1]) is not None, f"expected={r'ones=<int>'!r} actual={lines[1]!r}"


def test_values_match_number_digits():
    mod, out = _run_module_capture()
    lines = _parse_output(out)

    m1 = re.fullmatch(r"tens=(-?\d+)", lines[0])
    m2 = re.fullmatch(r"ones=(-?\d+)", lines[1])
    assert m1 and m2

    printed_tens = int(m1.group(1))
    printed_ones = int(m2.group(1))

    number = getattr(mod, "number")
    expected_tens = (number // 10) % 10
    expected_ones = number % 10

    assert printed_tens == expected_tens, f"expected={expected_tens!r} actual={printed_tens!r}"
    assert printed_ones == expected_ones, f"expected={expected_ones!r} actual={printed_ones!r}"


def test_variables_exist_and_are_ints():
    mod, out = _run_module_capture()
    assert hasattr(mod, "tens"), f"expected={True!r} actual={False!r}"
    assert hasattr(mod, "ones"), f"expected={True!r} actual={False!r}"
    assert isinstance(mod.tens, int), f"expected={int!r} actual={type(mod.tens)!r}"
    assert isinstance(mod.ones, int), f"expected={int!r} actual={type(mod.ones)!r}"


def test_printed_values_match_variables():
    mod, out = _run_module_capture()
    lines = _parse_output(out)

    printed_tens = int(lines[0].split("=", 1)[1])
    printed_ones = int(lines[1].split("=", 1)[1])

    assert printed_tens == mod.tens, f"expected={mod.tens!r} actual={printed_tens!r}"
    assert printed_ones == mod.ones, f"expected={mod.ones!r} actual={printed_ones!r}"