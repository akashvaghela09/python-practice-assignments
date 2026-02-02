import importlib.util
import os
import sys
import types


def _load_module(path, name="student_mod"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_counts(sentence, vowels):
    out = []
    for w in sentence.split():
        c = 0
        for ch in w:
            if ch in vowels:
                c += 1
        out.append((w, c))
    return out


def test_results_exists_and_is_list():
    path = os.path.join(os.path.dirname(__file__), "06_nestedLoops_countVowelsPerWord.py")
    mod = _load_module(path)

    assert hasattr(mod, "results")
    assert isinstance(mod.results, list)


def test_counts_for_default_sentence():
    path = os.path.join(os.path.dirname(__file__), "06_nestedLoops_countVowelsPerWord.py")
    mod = _load_module(path)

    assert hasattr(mod, "sentence")
    assert hasattr(mod, "vowels")
    assert hasattr(mod, "words")
    assert hasattr(mod, "results")

    expected = _expected_counts(mod.sentence, mod.vowels)
    actual = mod.results
    assert actual == expected, f"expected={expected} actual={actual}"


def test_words_match_sentence_split():
    path = os.path.join(os.path.dirname(__file__), "06_nestedLoops_countVowelsPerWord.py")
    mod = _load_module(path)

    expected = mod.sentence.split()
    actual = mod.words
    assert actual == expected, f"expected={expected} actual={actual}"


def test_results_structure_matches_words():
    path = os.path.join(os.path.dirname(__file__), "06_nestedLoops_countVowelsPerWord.py")
    mod = _load_module(path)

    expected_len = len(mod.words)
    actual_len = len(mod.results)
    assert actual_len == expected_len, f"expected={expected_len} actual={actual_len}"

    expected_words = mod.words
    actual_words = [t[0] for t in mod.results] if all(isinstance(t, tuple) and len(t) == 2 for t in mod.results) else mod.results
    assert actual_words == expected_words, f"expected={expected_words} actual={actual_words}"

    assert all(isinstance(t, tuple) and len(t) == 2 for t in mod.results)
    assert all(isinstance(t[0], str) for t in mod.results)
    assert all(isinstance(t[1], int) for t in mod.results)


def test_idempotent_reload_same_results():
    path = os.path.join(os.path.dirname(__file__), "06_nestedLoops_countVowelsPerWord.py")

    mod1 = _load_module(path, name="student_mod1")
    mod2 = _load_module(path, name="student_mod2")

    expected = _expected_counts(mod1.sentence, mod1.vowels)
    assert mod1.results == expected, f"expected={expected} actual={mod1.results}"
    assert mod2.results == expected, f"expected={expected} actual={mod2.results}"