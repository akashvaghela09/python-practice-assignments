import importlib.util
import sys
from pathlib import Path
import pytest


def run_script_with_input(monkeypatch, capsys, inputs):
    script_path = Path(__file__).with_name("04_passwordAttempts.py")
    spec = importlib.util.spec_from_file_location("password_attempts_mod", script_path)
    mod = importlib.util.module_from_spec(spec)

    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass

    out = capsys.readouterr().out
    return out


def assert_single_line_output(out, expected_line):
    lines = out.splitlines()
    assert len(lines) == 1, f"expected_lines=1 actual_lines={len(lines)}"
    actual = lines[0]
    assert actual == expected_line, f"expected={expected_line!r} actual={actual!r}"


def test_granted_on_first_try(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["opensesame"])
    assert_single_line_output(out, "Access granted")


def test_granted_on_second_try(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["wrong", "opensesame"])
    assert_single_line_output(out, "Access granted")


def test_granted_on_third_try(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["nope", "bad", "opensesame"])
    assert_single_line_output(out, "Access granted")


def test_denied_after_three_wrong(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["a", "b", "c"])
    assert_single_line_output(out, "Access denied")


def test_denied_with_more_than_three_inputs_ignores_extra(monkeypatch, capsys):
    out = run_script_with_input(monkeypatch, capsys, ["x", "y", "z", "opensesame"])
    assert_single_line_output(out, "Access denied")