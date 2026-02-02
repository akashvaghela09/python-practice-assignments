import importlib.util
import pathlib
import sys
import re

import pytest


def _load_module_from_path(path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(name, None)
    spec.loader.exec_module(module)
    return module


def test_output_matches_expected(capsys):
    path = pathlib.Path(__file__).resolve().parent / "09_countVowels.py"
    _load_module_from_path(path)
    out = capsys.readouterr().out
    expected = "vowels: 5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_single_line_with_correct_format(capsys):
    path = pathlib.Path(__file__).resolve().parent / "09_countVowels.py"
    _load_module_from_path(path)
    out = capsys.readouterr().out

    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_line_count = 1
    actual_line_count = len(lines)
    assert actual_line_count == expected_line_count, f"expected={expected_line_count!r} actual={actual_line_count!r}"

    m = re.fullmatch(r"vowels:\s*(\d+)", lines[0])
    expected_match = True
    actual_match = m is not None
    assert actual_match == expected_match, f"expected={expected_match!r} actual={actual_match!r}"

    expected_num = 5
    actual_num = int(m.group(1)) if m else None
    assert actual_num == expected_num, f"expected={expected_num!r} actual={actual_num!r}"


def test_module_has_expected_variables_after_run():
    path = pathlib.Path(__file__).resolve().parent / "09_countVowels.py"
    mod = _load_module_from_path(path)

    expected_text = "education"
    actual_text = getattr(mod, "text", None)
    assert actual_text == expected_text, f"expected={expected_text!r} actual={actual_text!r}"

    expected_vowels = "aeiou"
    actual_vowels = getattr(mod, "vowels", None)
    assert actual_vowels == expected_vowels, f"expected={expected_vowels!r} actual={actual_vowels!r}"

    expected_count = 5
    actual_count = getattr(mod, "count", None)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"