import importlib.util
import sys
import re
import types
from pathlib import Path

import pytest


MODULE_NAME = "12_validateIsogram"
FILE_NAME = "12_validateIsogram.py"


def _load_module():
    path = Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def _expected_is_isogram(text: str) -> bool:
    cleaned = text.lower().replace("-", "").replace(" ", "")
    letters = [c for c in cleaned if c.isalpha()]
    return len(set(letters)) == len(letters)


def test_import_prints_two_lines_true_false(capsys):
    _load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2, f"expected=2 actual={len(out)}"
    assert out[0] in ("True", "False"), f"expected=bool-string actual={out[0]!r}"
    assert out[1] in ("True", "False"), f"expected=bool-string actual={out[1]!r}"
    assert out[0] == "True", f"expected={'True'} actual={out[0]!r}"
    assert out[1] == "False", f"expected={'False'} actual={out[1]!r}"


@pytest.mark.parametrize(
    "text",
    [
        "six-year",
        "programming",
        "Dermatoglyphics",
        "aba",
        "a b a",
        "a-b-a",
        "isogram",
        "background",
        "thumbscrew-japingly",
        "Alphabet",
        "",
        "   ",
        "---",
        "H E-L L O",
        "no repeats",
        "re-peat",
        "Iñtërnâtiônàlizætiøn",
    ],
)
def test_is_isogram_matches_reference(text):
    mod = _load_module()
    assert hasattr(mod, "is_isogram"), "expected=function actual=missing"
    actual = mod.is_isogram(text)
    expected = _expected_is_isogram(text)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_is_isogram_returns_bool_type():
    mod = _load_module()
    result = mod.is_isogram("six-year")
    assert isinstance(result, bool), f"expected={bool} actual={type(result)}"


def test_ignores_hyphens_and_spaces_only_for_duplicates():
    mod = _load_module()
    text = "a - b - c"
    actual = mod.is_isogram(text)
    expected = _expected_is_isogram(text)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_non_letters_are_ignored_for_repeat_check():
    mod = _load_module()
    text = "a1a"
    actual = mod.is_isogram(text)
    expected = _expected_is_isogram(text)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_case_insensitive():
    mod = _load_module()
    text = "Aa"
    actual = mod.is_isogram(text)
    expected = _expected_is_isogram(text)
    assert actual == expected, f"expected={expected} actual={actual}"