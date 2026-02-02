import importlib.util
import os
import sys
import types
import pytest


FILE_NAME = "02_printWithIndexStart1.py"


def _load_module(path):
    name = "student_mod_02_printWithIndexStart1"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prints_expected_lines(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    mod = _load_module(path)
    out = capsys.readouterr().out
    expected = "1: red\n2: green\n3: blue\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_traceback_printed(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    _load_module(path)
    err = capsys.readouterr().err
    assert "Traceback" not in err, f"expected={False!r} actual={('Traceback' in err)!r}"


def test_colors_list_unchanged(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    mod = _load_module(path)
    _ = capsys.readouterr()
    expected = ["red", "green", "blue"]
    actual = getattr(mod, "colors", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"