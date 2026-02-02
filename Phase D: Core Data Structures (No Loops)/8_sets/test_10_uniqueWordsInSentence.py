import importlib.util
import os
import sys
import types
import pytest


FILE_NAME = "10_uniqueWordsInSentence.py"


def run_script(path):
    spec = importlib.util.spec_from_file_location("student_mod_10_unique", path)
    mod = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    sys.stdout = types.SimpleNamespace(write=lambda s: out.append(s))
    try:
        out.clear()
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout
    return "".join(out), mod


out = []


def test_file_exists():
    assert os.path.exists(FILE_NAME)


def test_script_runs_and_prints_expected_length():
    output, mod = run_script(FILE_NAME)
    lines = [ln.strip() for ln in output.splitlines() if ln.strip() != ""]
    expected = "5"
    actual = lines[-1] if lines else ""
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_words_is_set_of_unique_lowercase_words():
    _, mod = run_script(FILE_NAME)
    assert hasattr(mod, "words")
    assert isinstance(mod.words, set)
    expected = {"the", "cat", "sat", "on", "mat"}
    actual = mod.words
    assert actual == expected, f"expected={sorted(expected)!r} actual={sorted(actual)!r}"


def test_no_empty_string_in_words():
    _, mod = run_script(FILE_NAME)
    expected = False
    actual = "" in mod.words
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_all_words_lowercase():
    _, mod = run_script(FILE_NAME)
    expected = True
    actual = all(isinstance(w, str) and w == w.lower() for w in mod.words)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"