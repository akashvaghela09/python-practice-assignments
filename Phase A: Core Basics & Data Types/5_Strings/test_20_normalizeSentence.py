import importlib.util
import os
import sys
import re
import pytest


def _load_module():
    path = os.path.join(os.path.dirname(__file__), "20_normalizeSentence.py")
    spec = importlib.util.spec_from_file_location("normalizeSentence20", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout(monkeypatch):
    path = os.path.join(os.path.dirname(__file__), "20_normalizeSentence.py")
    out = []

    class _Stdout:
        def write(self, s):
            out.append(s)

        def flush(self):
            pass

    monkeypatch.setattr(sys, "stdout", _Stdout())
    spec = importlib.util.spec_from_file_location("normalizeSentence20_exec", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return "".join(out)


def _normalize_expected(s: str) -> str:
    return " ".join(s.strip().split()).lower()


def test_prints_normalized_sentence(monkeypatch):
    mod = _load_module()
    expected = _normalize_expected(mod.sentence)
    actual = _run_script_capture_stdout(monkeypatch).strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_normalized_variable_is_string_and_correct():
    mod = _load_module()
    assert hasattr(mod, "normalized")
    assert isinstance(mod.normalized, str)
    expected = _normalize_expected(mod.sentence)
    actual = mod.normalized
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_leading_or_trailing_spaces_in_normalized():
    mod = _load_module()
    expected = _normalize_expected(mod.sentence)
    actual = mod.normalized
    assert actual == actual.strip(), f"expected={expected!r} actual={actual!r}"


def test_no_multiple_internal_spaces_in_normalized():
    mod = _load_module()
    expected = _normalize_expected(mod.sentence)
    actual = mod.normalized
    assert re.search(r"\s{2,}", actual) is None, f"expected={expected!r} actual={actual!r}"


def test_is_all_lowercase_in_normalized():
    mod = _load_module()
    expected = _normalize_expected(mod.sentence)
    actual = mod.normalized
    assert actual == actual.lower(), f"expected={expected!r} actual={actual!r}"