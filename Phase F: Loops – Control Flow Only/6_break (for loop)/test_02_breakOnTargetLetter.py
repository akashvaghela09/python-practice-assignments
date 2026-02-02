import importlib.util
import os
import sys
import pytest


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_prints_chars_until_exclamation(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "02_breakOnTargetLetter.py")
    module_name = "break_on_target_letter_02"
    _load_module(module_name, file_path)

    out = capsys.readouterr().out
    actual_lines = [line.rstrip("\r") for line in out.splitlines() if line.strip() != ""]

    expected_lines = list("Hello")

    assert actual_lines == expected_lines, f"expected={expected_lines} actual={actual_lines}"


def test_does_not_print_exclamation(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "02_breakOnTargetLetter.py")
    module_name = "break_on_target_letter_02_no_bang"
    _load_module(module_name, file_path)

    out = capsys.readouterr().out
    assert "!" not in out, f"expected={'! not in output'} actual={out!r}"


def test_prints_each_character_on_separate_line(capsys):
    file_path = os.path.join(os.path.dirname(__file__), "02_breakOnTargetLetter.py")
    module_name = "break_on_target_letter_02_line_format"
    _load_module(module_name, file_path)

    out = capsys.readouterr().out
    lines = out.splitlines()
    nonempty = [ln for ln in lines if ln.strip() != ""]

    expected_count = 5
    actual_count = len(nonempty)
    assert actual_count == expected_count, f"expected={expected_count} actual={actual_count}"

    expected_lengths = [1] * expected_count
    actual_lengths = [len(ln.strip()) for ln in nonempty]
    assert actual_lengths == expected_lengths, f"expected={expected_lengths} actual={actual_lengths}"