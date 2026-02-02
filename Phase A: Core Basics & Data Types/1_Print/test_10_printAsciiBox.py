import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "10_printAsciiBox.py"
MODULE_NAME = "printAsciiBox10"


def run_student_script():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    assert os.path.exists(path)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    out = buf.getvalue()
    return module, out


def test_prints_exact_box_output():
    module, out = run_student_script()
    expected_lines = ["+----------+", "|  Python  |", "+----------+"]
    expected = "\n".join(expected_lines) + "\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_three_lines_only_and_no_extra_whitespace():
    module, out = run_student_script()
    lines = out.splitlines()
    assert len(lines) == 3, f"expected={3!r} actual={len(lines)!r}"
    for i, line in enumerate(lines):
        assert line == line.rstrip("\r\n"), f"expected={line.rstrip(chr(10)+chr(13))!r} actual={line!r}"


def test_line_lengths_and_structure():
    module, out = run_student_script()
    lines = out.splitlines()
    assert len(lines) == 3, f"expected={3!r} actual={len(lines)!r}"

    for idx in (0, 2):
        assert len(lines[idx]) == 12, f"expected={12!r} actual={len(lines[idx])!r}"
        assert lines[idx].startswith("+") and lines[idx].endswith("+"), f"expected={(True, True)!r} actual={(lines[idx].startswith('+'), lines[idx].endswith('+'))!r}"
        middle = lines[idx][1:-1]
        assert set(middle) <= {"-"}, f"expected={{'-'}!r} actual={set(middle)!r}"

    mid = lines[1]
    assert len(mid) == 12, f"expected={12!r} actual={len(mid)!r}"
    assert mid[0] == "|" and mid[-1] == "|", f"expected={('|','|')!r} actual={(mid[0], mid[-1])!r}"
    inside = mid[1:-1]
    assert inside == "  Python  ", f"expected={'  Python  '!r} actual={inside!r}"


def test_no_triple_quoted_string_used_for_full_output():
    path = os.path.join(os.getcwd(), MODULE_FILENAME)
    src = open(path, "r", encoding="utf-8").read()
    triple_double = '"""'
    triple_single = "'''"
    assert triple_double not in src and triple_single not in src, f"expected={False!r} actual={True!r}"


def test_defines_line_variables():
    module, out = run_student_script()
    assert hasattr(module, "line1"), f"expected={True!r} actual={hasattr(module, 'line1')!r}"
    assert hasattr(module, "line2"), f"expected={True!r} actual={hasattr(module, 'line2')!r}"
    assert hasattr(module, "line3"), f"expected={True!r} actual={hasattr(module, 'line3')!r}"
    assert isinstance(module.line1, str), f"expected={str!r} actual={type(module.line1)!r}"
    assert isinstance(module.line2, str), f"expected={str!r} actual={type(module.line2)!r}"
    assert isinstance(module.line3, str), f"expected={str!r} actual={type(module.line3)!r}"