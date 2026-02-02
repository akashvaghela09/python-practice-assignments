import builtins
import importlib.util
import sys
from pathlib import Path

import pytest


MODULE_NAME = "03_passwordAttempts"
FILE_NAME = "03_passwordAttempts.py"


def load_module(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr(builtins, "input", fake_input)

    file_path = Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(MODULE_NAME, None)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(MODULE_NAME, None)
    return module


def assert_stdout_exact(capfd, expected):
    out = capfd.readouterr().out
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_access_granted_breaks_early(monkeypatch, capfd):
    load_module(monkeypatch, ["java", "ruby", "python", "should_not_be_read"])
    assert_stdout_exact(capfd, "Access granted\n")


def test_access_denied_after_three_failures(monkeypatch, capfd):
    load_module(monkeypatch, ["java", "ruby", "go"])
    assert_stdout_exact(capfd, "Access denied\n")


def test_access_granted_on_first_try(monkeypatch, capfd):
    load_module(monkeypatch, ["python", "extra"])
    assert_stdout_exact(capfd, "Access granted\n")


def test_access_granted_on_third_try(monkeypatch, capfd):
    load_module(monkeypatch, ["nope", "still_no", "python", "extra"])
    assert_stdout_exact(capfd, "Access granted\n")


def test_no_output_if_input_exhausted_early(monkeypatch, capfd):
    with pytest.raises(EOFError):
        load_module(monkeypatch, [])
    assert_stdout_exact(capfd, "")