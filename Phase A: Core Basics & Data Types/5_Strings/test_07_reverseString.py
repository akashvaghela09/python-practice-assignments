import importlib.util
import os
import sys
import types


def _load_module(path, module_name="mod_under_test"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_reversed_string(capsys):
    path = os.path.join(os.path.dirname(__file__), "07_reverseString.py")
    _load_module(path, "reverse_string_module_1")
    out = capsys.readouterr().out
    assert out == "nohtyp\n", f"expected={'nohtyp\\n'!r} actual={out!r}"


def test_rev_variable_is_reversed_string(capsys):
    path = os.path.join(os.path.dirname(__file__), "07_reverseString.py")
    mod = _load_module(path, "reverse_string_module_2")
    capsys.readouterr()
    actual = getattr(mod, "rev", None)
    expected = getattr(mod, "word")[::-1]
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_word_unchanged(capsys):
    path = os.path.join(os.path.dirname(__file__), "07_reverseString.py")
    mod = _load_module(path, "reverse_string_module_3")
    capsys.readouterr()
    assert getattr(mod, "word") == "python", f"expected={'python'!r} actual={getattr(mod, 'word')!r}"