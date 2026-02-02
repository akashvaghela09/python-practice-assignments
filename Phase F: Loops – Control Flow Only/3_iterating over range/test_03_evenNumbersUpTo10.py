import importlib.util
import io
import os
import sys
import pytest

MODULE_FILENAME = "03_evenNumbersUpTo10.py"


def load_module_from_file(tmp_path, source_text):
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(source_text, encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_module", str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_file_capture_stdout(file_path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("student_run", str(file_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_program_runs_without_placeholders(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    assert os.path.exists(src_path), f"missing={MODULE_FILENAME}"
    src = open(src_path, "r", encoding="utf-8").read()
    assert "____" not in src
    load_module_from_file(tmp_path, src)


def test_prints_even_numbers_0_to_10_each_on_own_line(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    src = open(src_path, "r", encoding="utf-8").read()
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(src, encoding="utf-8")

    out = run_file_capture_stdout(file_path)

    expected_lines = ["0", "2", "4", "6", "8", "10"]
    actual_lines = out.splitlines()

    assert expected_lines == actual_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_no_extra_whitespace_on_lines(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    src = open(src_path, "r", encoding="utf-8").read()
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(src, encoding="utf-8")

    out = run_file_capture_stdout(file_path)
    actual_lines = out.splitlines()
    trimmed_lines = [line.strip() for line in actual_lines]

    assert trimmed_lines == actual_lines, f"expected={trimmed_lines!r} actual={actual_lines!r}"


def test_ends_with_newline(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    src = open(src_path, "r", encoding="utf-8").read()
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(src, encoding="utf-8")

    out = run_file_capture_stdout(file_path)
    expected = True
    actual = (out == "") or out.endswith("\n")
    assert expected == actual, f"expected={expected!r} actual={actual!r}"