import importlib.util
import os
import sys
import pytest

MODULE_FILE = "10_iterateByIndex.py"


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location("mod_under_test_10", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_no_placeholders_left():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    assert "____" not in src, "Expected no placeholders, found placeholders"


def test_prints_even_index_letters_each_on_new_line(capsys):
    _run_module_capture_stdout()
    out = capsys.readouterr().out
    expected = "a\nc\ne\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_exactly_three_lines(capsys):
    _run_module_capture_stdout()
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln != ""]
    expected_count = 3
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_printed_values_match_list_even_indices(capsys):
    mod = _run_module_capture_stdout()
    out = capsys.readouterr().out
    printed = out.splitlines()
    expected = [mod.letters[i] for i in range(len(mod.letters)) if i % 2 == 0]
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_no_extra_whitespace_on_lines(capsys):
    _run_module_capture_stdout()
    out = capsys.readouterr().out
    lines = out.splitlines()
    stripped = [ln.strip() for ln in lines]
    assert lines == stripped, f"expected={stripped!r} actual={lines!r}"