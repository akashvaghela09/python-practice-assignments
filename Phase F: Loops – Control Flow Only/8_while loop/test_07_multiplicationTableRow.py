import importlib.util
import os
import sys
import types
import pytest

MODULE_FILENAME = "07_multiplicationTableRow.py"


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("student_module_07", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected_output_lines():
    base = 7
    return [f"{base} x {i} = {base*i}" for i in range(1, 6)]


def test_file_exists():
    assert os.path.exists(MODULE_FILENAME)


def test_no_placeholders_left_in_source():
    with open(MODULE_FILENAME, "r", encoding="utf-8") as f:
        src = f.read()
    assert "__________" not in src


def test_prints_exact_table(capsys):
    _load_module_from_path(MODULE_FILENAME)
    out = capsys.readouterr().out
    expected = "\n".join(_expected_output_lines()) + "\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_only_five_lines_and_correct_format(capsys):
    _load_module_from_path(MODULE_FILENAME)
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_lines = _expected_output_lines()
    assert len(lines) == 5, f"expected={len(expected_lines)!r} actual={len(lines)!r}"
    for exp, act in zip(expected_lines, lines):
        assert act == exp, f"expected={exp!r} actual={act!r}"


def test_no_extra_output_whitespace(capsys):
    _load_module_from_path(MODULE_FILENAME)
    out = capsys.readouterr().out
    lines = out.splitlines()
    expected_lines = _expected_output_lines()
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"