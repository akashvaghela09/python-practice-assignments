import importlib.util
import os
import sys
import types
import pytest


def load_module_from_filename(filename):
    module_name = os.path.splitext(os.path.basename(filename))[0]
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_is_single_line_and_correct(capsys):
    load_module_from_filename("09_countCharacters.py")
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"
    assert lines[0] == "length=6", f"expected={'length=6'!r} actual={lines[0]!r}"


def test_length_variable_exists_and_is_int(capsys):
    mod = load_module_from_filename("09_countCharacters.py")
    assert hasattr(mod, "length"), f"expected={True!r} actual={hasattr(mod, 'length')!r}"
    assert isinstance(mod.length, int), f"expected={int!r} actual={type(mod.length)!r}"


def test_length_matches_len_of_word(capsys):
    mod = load_module_from_filename("09_countCharacters.py")
    assert hasattr(mod, "word"), f"expected={True!r} actual={hasattr(mod, 'word')!r}"
    expected = len(mod.word)
    actual = mod.length
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_word_value_is_python(capsys):
    mod = load_module_from_filename("09_countCharacters.py")
    assert mod.word == "python", f"expected={'python'!r} actual={mod.word!r}"