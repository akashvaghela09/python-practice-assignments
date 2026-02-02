import importlib.util
import os
import sys
import builtins
import pytest

MODULE_FILE = "02_greetByName.py"


def load_module(monkeypatch):
    spec = importlib.util.spec_from_file_location("mod_02_greetByName", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_greet_function_exists_and_returns_expected(monkeypatch):
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)
    mod = load_module(monkeypatch)
    assert hasattr(mod, "greet")
    assert callable(mod.greet)

    expected = "Hello, Ava!"
    actual = mod.greet("Ava")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_module_prints_expected_on_import(monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        captured.append(" ".join(str(a) for a in args))

    monkeypatch.setattr(builtins, "print", fake_print)
    load_module(monkeypatch)

    expected_lines = ["Hello, Ava!"]
    actual_lines = captured[:1]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_greet_handles_other_name(monkeypatch):
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)
    mod = load_module(monkeypatch)

    expected = "Hello, Sam!"
    actual = mod.greet("Sam")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"