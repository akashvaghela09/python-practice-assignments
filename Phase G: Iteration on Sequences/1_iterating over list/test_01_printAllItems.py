import importlib.util
import io
import os
import sys
import pytest


def _load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_each_fruit_on_own_line(capsys):
    path = os.path.join(os.path.dirname(__file__), "01_printAllItems.py")
    _load_module(path)
    out = capsys.readouterr().out
    expected = "apple\nbanana\ncherry\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output(capsys):
    path = os.path.join(os.path.dirname(__file__), "01_printAllItems.py")
    _load_module(path)
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines()]
    expected_lines = ["apple", "banana", "cherry"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"


def test_import_executes_without_errors():
    path = os.path.join(os.path.dirname(__file__), "01_printAllItems.py")
    _load_module(path)