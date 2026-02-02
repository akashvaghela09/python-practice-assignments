import importlib.util
import io
import os
import sys
import re
import pytest

FILE_NAME = "04_showIndexAndValue.py"


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        load_module_from_path(str(dst), "student_module_04")
    finally:
        sys.stdout = old
    return buf.getvalue()


def normalize_output(s):
    lines = [ln.rstrip("\n") for ln in s.splitlines()]
    lines = [ln.strip() for ln in lines if ln.strip() != ""]
    return lines


def test_no_placeholders_left():
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    content = open(src, "r", encoding="utf-8").read()
    assert "____" not in content


def test_expected_output_lines(tmp_path):
    out = run_script_capture_stdout(tmp_path)
    actual_lines = normalize_output(out)

    expected_lines = ["0: red", "1: blue", "2: green"]
    assert len(actual_lines) == len(expected_lines), f"expected={len(expected_lines)} actual={len(actual_lines)}"
    for e, a in zip(expected_lines, actual_lines):
        assert a == e, f"expected={e!r} actual={a!r}"


def test_output_format_strict_indices(tmp_path):
    out = run_script_capture_stdout(tmp_path)
    lines = normalize_output(out)
    for i, line in enumerate(lines):
        m = re.fullmatch(r"(\d+):\s*(.+)", line)
        assert m is not None, f"expected={'<index>: <value>'!r} actual={line!r}"
        idx = int(m.group(1))
        assert idx == i, f"expected={i!r} actual={idx!r}"


def test_produces_exactly_three_prints(tmp_path):
    out = run_script_capture_stdout(tmp_path)
    lines = normalize_output(out)
    assert len(lines) == 3, f"expected={3!r} actual={len(lines)!r}"