import importlib.util
import io
import os
import contextlib

MODULE_NAME = "02_skipVowels"
FILE_NAME = "02_skipVowels.py"


def _run_module_capture_stdout():
    here = os.path.dirname(__file__)
    path = os.path.join(here, FILE_NAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return buf.getvalue()


def test_output_matches_expected():
    out = _run_module_capture_stdout()
    expected = "Pythn\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_single_line_with_newline():
    out = _run_module_capture_stdout()
    assert out.endswith("\n"), f"expected={True!r} actual={out.endswith(chr(10))!r}"
    lines = out.splitlines()
    assert len(lines) == 1, f"expected={1!r} actual={len(lines)!r}"


def test_no_vowels_in_output():
    out = _run_module_capture_stdout()
    line = out.splitlines()[0] if out else ""
    vowels = set("aeiouAEIOU")
    has_vowel = any(ch in vowels for ch in line)
    assert has_vowel is False, f"expected={False!r} actual={has_vowel!r}"


def test_preserves_order_of_remaining_characters():
    out = _run_module_capture_stdout()
    actual = out.splitlines()[0] if out else ""
    text = "Python"
    expected = "".join(ch for ch in text if ch not in "aeiouAEIOU")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_no_spaces_or_extra_characters():
    out = _run_module_capture_stdout()
    line = out.splitlines()[0] if out else ""
    extra = any(ch.isspace() for ch in line)
    assert extra is False, f"expected={False!r} actual={extra!r}"