import builtins
import importlib.util
import io
import os
import sys
import pytest

MODULE_FILE = "10_menuLoopCalculator.py"


def load_module(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr(builtins, "input", fake_input)

    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)

    spec = importlib.util.spec_from_file_location("menu_calc_10", os.path.join(os.getcwd(), MODULE_FILE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return buf.getvalue()


def norm_lines(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if s.endswith("\n"):
        s = s[:-1]
    return s.split("\n") if s else []


def test_quit_only_prints_bye(monkeypatch):
    out = load_module(monkeypatch, ["quit"])
    lines = norm_lines(out)
    assert lines == ["Bye"], f"expected={['Bye']!r} actual={lines!r}"


def test_add_sub_mul_div_then_quit(monkeypatch):
    inputs = [
        "add", "2", "3",
        "sub", "10", "4",
        "mul", "1.5", "2",
        "div", "9", "3",
        "quit",
    ]
    out = load_module(monkeypatch, inputs)
    lines = norm_lines(out)
    expected = ["5.0", "6.0", "3.0", "3.0", "Bye"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_division_by_zero_prints_message_and_continues(monkeypatch):
    inputs = [
        "div", "5", "0",
        "add", "1", "2",
        "quit",
    ]
    out = load_module(monkeypatch, inputs)
    lines = norm_lines(out)
    expected = ["Cannot divide by zero", "3.0", "Bye"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_float_handling_and_negative_values(monkeypatch):
    inputs = [
        "add", "-1.25", "2.5",
        "sub", "0", "-3.5",
        "mul", "-2", "-4",
        "div", "-7.5", "2.5",
        "quit",
    ]
    out = load_module(monkeypatch, inputs)
    lines = norm_lines(out)
    expected = ["1.25", "3.5", "8.0", "-3.0", "Bye"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_no_extra_output_lines(monkeypatch):
    inputs = [
        "add", "0", "0",
        "quit",
    ]
    out = load_module(monkeypatch, inputs)
    lines = norm_lines(out)
    expected = ["0.0", "Bye"]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"