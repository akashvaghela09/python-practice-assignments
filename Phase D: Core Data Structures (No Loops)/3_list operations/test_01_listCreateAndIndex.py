import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

EXPECTED_LINES = ["first=10", "last=50"]


def _run_student_module():
    path = os.path.join(os.path.dirname(__file__), "01_listCreateAndIndex.py")
    spec = importlib.util.spec_from_file_location("listCreateAndIndex_01", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    output = buf.getvalue()
    return module, output


def _normalize_lines(s: str):
    lines = [ln.strip() for ln in s.splitlines() if ln.strip() != ""]
    return lines


def test_module_runs_without_error_and_prints_expected_lines():
    module, out = _run_student_module()
    lines = _normalize_lines(out)

    expected = EXPECTED_LINES
    actual = lines[-2:] if len(lines) >= 2 else lines
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_first_and_last_values_are_correct():
    module, out = _run_student_module()

    assert hasattr(module, "numbers"), "expected=True actual=False"
    assert hasattr(module, "first"), "expected=True actual=False"
    assert hasattr(module, "last"), "expected=True actual=False"

    expected_first = 10
    expected_last = 50
    assert module.first == expected_first, f"expected={expected_first!r} actual={module.first!r}"
    assert module.last == expected_last, f"expected={expected_last!r} actual={module.last!r}"


def test_numbers_list_structure():
    module, out = _run_student_module()

    expected_numbers = [10, 20, 30, 40, 50]
    assert module.numbers == expected_numbers, f"expected={expected_numbers!r} actual={module.numbers!r}"


def test_output_contains_correct_key_value_format():
    module, out = _run_student_module()
    lines = _normalize_lines(out)

    exp_pattern_first = r"^first=\d+$"
    exp_pattern_last = r"^last=\d+$"

    expected = True
    actual = bool(lines) and re.match(exp_pattern_first, lines[0]) is not None
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    expected = True
    actual = len(lines) >= 2 and re.match(exp_pattern_last, lines[1]) is not None
    assert actual == expected, f"expected={expected!r} actual={actual!r}"