import importlib.util
import pathlib
import re
import sys
import types
import pytest

MODULE_NAME = "09_stringPipeline"
FILE_NAME = "09_stringPipeline.py"


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expect_remove_punctuation(s: str) -> str:
    return s.translate(str.maketrans("", "", ",.!"))


def _expect_collapse_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def _expect_clean_sentence(s: str) -> str:
    return _expect_collapse_spaces(_expect_remove_punctuation(s)).strip()


def test_remove_punctuation_basic():
    mod = _load_module()
    s = "a,b.c! d"
    expected = _expect_remove_punctuation(s)
    actual = mod.remove_punctuation(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_remove_punctuation_only_targets_specific_chars():
    mod = _load_module()
    s = "keep:;?-'\"()[]{}@#"
    expected = _expect_remove_punctuation(s)
    actual = mod.remove_punctuation(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_remove_punctuation_idempotent():
    mod = _load_module()
    s = "Hi,,  world!!..."
    once = mod.remove_punctuation(s)
    twice = mod.remove_punctuation(once)
    assert twice == once, f"expected={once!r} actual={twice!r}"


def test_collapse_spaces_collapses_whitespace_runs():
    mod = _load_module()
    s = "a\t\tb\n\nc   d"
    expected = _expect_collapse_spaces(s)
    actual = mod.collapse_spaces(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_collapse_spaces_preserves_non_whitespace():
    mod = _load_module()
    s = "  x  y\tz\nw  "
    expected = _expect_collapse_spaces(s)
    actual = mod.collapse_spaces(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clean_sentence_pipeline_order_and_strip():
    mod = _load_module()
    s = " \tHi,,  world!!  \n"
    expected = _expect_clean_sentence(s)
    actual = mod.clean_sentence(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clean_sentence_no_punctuation_only_space_collapse_and_strip():
    mod = _load_module()
    s = "  alpha\t beta \n gamma  "
    expected = _expect_clean_sentence(s)
    actual = mod.clean_sentence(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clean_sentence_empty_and_whitespace_only():
    mod = _load_module()
    s = " \t \n "
    expected = _expect_clean_sentence(s)
    actual = mod.clean_sentence(s)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_functions_return_str_type():
    mod = _load_module()
    assert isinstance(mod.remove_punctuation("x"), str)
    assert isinstance(mod.collapse_spaces("x"), str)
    assert isinstance(mod.clean_sentence("x"), str)