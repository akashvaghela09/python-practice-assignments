import importlib
import sys
import types
import pytest


MODULE_NAME = "04_defaultParameter"


def _load_module():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def test_repeat_word_exists_and_callable():
    m = _load_module()
    assert hasattr(m, "repeat_word")
    assert callable(m.repeat_word)


def test_repeat_word_default_times_repeats_twice():
    m = _load_module()
    expected = "go go"
    actual = m.repeat_word("go")
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_repeat_word_three_times():
    m = _load_module()
    expected = "go go go"
    actual = m.repeat_word("go", 3)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_repeat_word_single_time_no_extra_spaces():
    m = _load_module()
    expected = "hi"
    actual = m.repeat_word("hi", 1)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_repeat_word_preserves_word_exactly():
    m = _load_module()
    expected = "a  b a  b"
    actual = m.repeat_word("a  b", 2)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_module_prints_expected_output_on_import(capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    importlib.import_module(MODULE_NAME)
    captured = capsys.readouterr()
    expected = "go go\ngo go go\n"
    actual = captured.out
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_repeat_word_signature_has_default_2():
    m = _load_module()
    import inspect

    sig = inspect.signature(m.repeat_word)
    params = list(sig.parameters.values())
    assert len(params) >= 2
    assert params[0].name == "word"
    assert params[1].name == "times"
    expected = 2
    actual = params[1].default
    assert expected == actual, f"expected={expected!r} actual={actual!r}"