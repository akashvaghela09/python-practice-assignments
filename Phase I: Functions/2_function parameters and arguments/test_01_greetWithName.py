import importlib.util
import io
import os
import sys
import pytest


def _load_module():
    fname = "01_greetWithName.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("mod_01_greetWithName", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_running_file_prints_exact_output(capsys):
    _load_module()
    captured = capsys.readouterr()
    expected = "Hello, Ada!\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_greet_returns_string_for_various_names(capsys):
    m = _load_module()
    capsys.readouterr()

    cases = [
        ("Ada", "Hello, Ada!"),
        ("Bob", "Hello, Bob!"),
        ("", "Hello, !"),
        ("Jean-Luc", "Hello, Jean-Luc!"),
        ("  Ada  ", "Hello,   Ada  !"),
    ]
    for name, expected in cases:
        actual = m.greet(name)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_greet_requires_one_argument(capsys):
    m = _load_module()
    capsys.readouterr()
    with pytest.raises(TypeError):
        m.greet()  # type: ignore


def test_greet_does_not_print(capsys):
    m = _load_module()
    capsys.readouterr()
    _ = m.greet("Ada")
    captured = capsys.readouterr()
    expected = ""
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"