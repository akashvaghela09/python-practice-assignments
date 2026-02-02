import importlib.util
import os
import sys
import types
import pytest

MODULE_FILENAME = "02_fullNameFormatter.py"
MODULE_NAME = "fullNameFormatter_02_tests"


def _load_module_safely(path):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def test_running_file_prints_expected_output(capsys):
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    _load_module_safely(path)
    out = capsys.readouterr().out
    expected = "Lovelace, Ada\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_format_name_returns_last_comma_space_first():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    mod = _load_module_safely(path)
    assert hasattr(mod, "format_name")
    result = mod.format_name("Grace", "Hopper")
    expected = "Hopper, Grace"
    assert result == expected, f"expected={expected!r} actual={result!r}"


def test_format_name_requires_two_required_positional_args():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    mod = _load_module_safely(path)

    with pytest.raises(TypeError):
        mod.format_name("Ada")

    with pytest.raises(TypeError):
        mod.format_name()

    with pytest.raises(TypeError):
        mod.format_name("Ada", "Lovelace", "Extra")


def test_format_name_preserves_inputs_as_strings():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    mod = _load_module_safely(path)

    first = "  Ada "
    last = " Lovelace  "
    result = mod.format_name(first, last)
    expected = f"{last}, {first}"
    assert result == expected, f"expected={expected!r} actual={result!r}"