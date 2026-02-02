import importlib.util
import sys
from pathlib import Path
import pytest


MODULE_NAME = "01_countUpToN"
FILE_PATH = Path(__file__).with_name("01_countUpToN.py")


def run_script_with_input(monkeypatch, capsys, input_text):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(FILE_PATH))
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setattr(sys, "argv", [str(FILE_PATH)])
    monkeypatch.setattr("builtins.input", lambda: input_text)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return out


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, "1\n"),
        (3, "1\n2\n3\n"),
        (5, "1\n2\n3\n4\n5\n"),
    ],
)
def test_counts_up_inclusive(monkeypatch, capsys, n, expected):
    actual = run_script_with_input(monkeypatch, capsys, f"{n}\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_zero_prints_nothing(monkeypatch, capsys):
    expected = ""
    actual = run_script_with_input(monkeypatch, capsys, "0\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_negative_prints_nothing(monkeypatch, capsys):
    expected = ""
    actual = run_script_with_input(monkeypatch, capsys, "-7\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_ignores_surrounding_whitespace(monkeypatch, capsys):
    expected = "1\n2\n3\n4\n"
    actual = run_script_with_input(monkeypatch, capsys, "   4   \n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_extra_spaces_in_lines(monkeypatch, capsys):
    actual = run_script_with_input(monkeypatch, capsys, "4\n")
    lines = actual.splitlines()
    expected_lines = ["1", "2", "3", "4"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"


def test_trailing_newline_present_for_positive(monkeypatch, capsys):
    actual = run_script_with_input(monkeypatch, capsys, "2\n")
    expected = True
    got = actual.endswith("\n")
    assert got == expected, f"expected={expected!r} actual={got!r}"