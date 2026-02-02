import builtins
import importlib.util
import os
import sys
import pytest


MODULE_PATH = os.path.join(os.path.dirname(__file__), "05_averageUntilBlank.py")


def run_module_with_input(lines):
    it = iter(lines)

    def fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    spec = importlib.util.spec_from_file_location("avg_until_blank_mod", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)

    old_input = builtins.input
    builtins.input = fake_input
    try:
        spec.loader.exec_module(mod)
    finally:
        builtins.input = old_input


def test_no_data_prints_no_data(capsys):
    run_module_with_input([""])
    out = capsys.readouterr().out.strip()
    expected = "No data"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_average_rounds_to_two_decimals(capsys):
    run_module_with_input(["3", "4", "3", ""])
    out = capsys.readouterr().out.strip()
    expected = "3.33"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_accepts_floats_and_rounds(capsys):
    run_module_with_input(["1.2", "1.2", ""])
    out = capsys.readouterr().out.strip()
    expected = "1.20"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_negative_numbers_average(capsys):
    run_module_with_input(["-1", "1", ""])
    out = capsys.readouterr().out.strip()
    expected = "0.00"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_single_value_prints_with_two_decimals(capsys):
    run_module_with_input(["5", ""])
    out = capsys.readouterr().out.strip()
    expected = "5.00"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_trailing_whitespace_on_numbers_allowed(capsys):
    run_module_with_input(["2 ", "2", ""])
    out = capsys.readouterr().out.strip()
    expected = "2.00"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_multiple_outputs_not_expected(capsys):
    run_module_with_input(["1", "2", ""])
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_lines_count = 1
    assert len(lines) == expected_lines_count, f"expected={expected_lines_count!r} actual={len(lines)!r}"