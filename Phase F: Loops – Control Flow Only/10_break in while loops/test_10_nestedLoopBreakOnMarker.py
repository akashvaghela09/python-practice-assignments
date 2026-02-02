import builtins
import importlib.util
import io
import os
import sys
import pytest

MODULE_FILE = "10_nestedLoopBreakOnMarker.py"


def _run_module_with_input(lines):
    it = iter(lines)

    def fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    old_input = builtins.input
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    builtins.input = fake_input
    try:
        spec = importlib.util.spec_from_file_location("mod10_nestedLoopBreakOnMarker", MODULE_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = sys.stdout.getvalue()
    finally:
        builtins.input = old_input
        sys.stdout = old_stdout
    return output


def _expected_total(lines):
    total = 0
    for line in lines:
        if line.strip() == "END":
            break
        for token in line.split():
            n = int(token)
            if n == 0:
                break
            total += n
    return total


def _expected_output(lines):
    return f"Total: {_expected_total(lines)}\n"


def test_example_given():
    lines = ["1 2 0 100", "5 5", "9 0 9", "END"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_immediate_end():
    lines = ["END"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_zero_first_token_in_line():
    lines = ["0 1 2 3", "4 0 5", "END"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_negative_and_positive_numbers_with_zero_marker():
    lines = ["-1 -2 0 99", "3 -4 5", "END"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_multiple_lines_no_zeros_until_end():
    lines = ["1 2 3", "4 5 6", "7", "END"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_stops_on_end_even_if_more_inputs_exist():
    lines = ["1 2 3", "END", "999 999 0 999"]
    out = _run_module_with_input(lines)
    exp = _expected_output(lines)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_blank_line_then_numbers_then_end():
    lines = ["", "1 0 2", "END"]
    with pytest.raises(ValueError):
        _run_module_with_input(lines)