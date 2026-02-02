import importlib.util
import sys
from pathlib import Path
import pytest


ASSIGNMENT_FILE = "07_userInputVariables.py"


def run_script_with_input(monkeypatch, capsys, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        return next(it)

    monkeypatch.setattr("builtins.input", fake_input)

    script_path = Path(__file__).resolve().parent / ASSIGNMENT_FILE
    spec = importlib.util.spec_from_file_location("student_module_07", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["student_module_07"] = module
    spec.loader.exec_module(module)

    out = capsys.readouterr().out
    return out


def assert_single_line_exact(actual_out, expected_line):
    actual = actual_out
    expected = expected_line + "\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_given_example(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["Mia", "8"])
    assert_single_line_exact(out, "Mia will be 9 next year.")


def test_other_name_and_age(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["Leo", "0"])
    assert_single_line_exact(out, "Leo will be 1 next year.")


def test_whitespace_in_age_is_handled(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["Ana", "  41 "])
    assert_single_line_exact(out, "Ana will be 42 next year.")


def test_negative_age(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["Zed", "-1"])
    assert_single_line_exact(out, "Zed will be 0 next year.")


def test_name_with_spaces(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["Mary Jane", "17"])
    assert_single_line_exact(out, "Mary Jane will be 18 next year.")