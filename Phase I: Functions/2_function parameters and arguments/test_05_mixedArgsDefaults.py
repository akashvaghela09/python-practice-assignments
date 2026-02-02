import importlib.util
import pathlib
import sys
import pytest

MODULE_NAME = "05_mixedArgsDefaults"
FILE_PATH = pathlib.Path(__file__).with_name("05_mixedArgsDefaults.py")


def load_module():
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(FILE_PATH))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(MODULE_NAME, None)
    spec.loader.exec_module(module)
    return module


def test_welcome_function_exists_and_is_callable():
    mod = load_module()
    assert hasattr(mod, "welcome")
    assert callable(mod.welcome)


def test_welcome_defaults_and_overrides():
    mod = load_module()
    assert mod.welcome("Sam") == "Hi, Sam."
    assert mod.welcome("Sam", greeting="Hello", punctuation="!") == "Hello, Sam!"


def test_welcome_keyword_only_mix():
    mod = load_module()
    assert mod.welcome(name="Sam") == "Hi, Sam."
    assert mod.welcome("Sam", punctuation="?") == "Hi, Sam?"
    assert mod.welcome("Sam", greeting="Hey") == "Hey, Sam."
    assert mod.welcome(name="Sam", greeting="Yo", punctuation="!!!") == "Yo, Sam!!!"


def test_file_prints_exact_expected_output(capsys):
    load_module()
    out = capsys.readouterr().out
    expected = "Hi, Sam.\nHello, Sam!\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"