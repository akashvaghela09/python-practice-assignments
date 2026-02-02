import importlib.util
import io
import os
import sys
import re
import pytest

MODULE_FILE = "09_parseMixedBaseAndSum.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    spec = importlib.util.spec_from_file_location("student_mod_09", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    old_stdout = sys.stdout
    try:
        buf = io.StringIO()
        sys.stdout = buf
        spec = importlib.util.spec_from_file_location("student_run_09", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def parse_int_from_str_line(line):
    m = re.fullmatch(r"[+-]?\d+", line.strip())
    if not m:
        raise ValueError(f"non-integer output line: {line!r}")
    return int(line.strip())


def test_stdout_three_lines_and_numeric_sum_relation():
    out = run_script_capture_stdout()
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 3, f"expected_lines=3 actual_lines={len(lines)}"
    a = parse_int_from_str_line(lines[0])
    b = parse_int_from_str_line(lines[1])
    c = parse_int_from_str_line(lines[2])
    assert c == a + b, f"expected_sum={a + b} actual_sum={c}"


def test_n1_n2_exist_and_match_parsed_values():
    mod = load_module()
    assert hasattr(mod, "s1"), "expected_attr=s1 actual_attr_missing=s1"
    assert hasattr(mod, "s2"), "expected_attr=s2 actual_attr_missing=s2"
    assert hasattr(mod, "n1"), "expected_attr=n1 actual_attr_missing=n1"
    assert hasattr(mod, "n2"), "expected_attr=n2 actual_attr_missing=n2"

    exp_n1 = int(mod.s1, 0)
    exp_n2 = int(mod.s2, 16)

    assert isinstance(mod.n1, int), f"expected_type=int actual_type={type(mod.n1).__name__}"
    assert isinstance(mod.n2, int), f"expected_type=int actual_type={type(mod.n2).__name__}"

    assert mod.n1 == exp_n1, f"expected={exp_n1} actual={mod.n1}"
    assert mod.n2 == exp_n2, f"expected={exp_n2} actual={mod.n2}"


def test_printed_values_match_module_values():
    mod = load_module()
    out = run_script_capture_stdout()
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 3, f"expected_lines=3 actual_lines={len(lines)}"

    a = parse_int_from_str_line(lines[0])
    b = parse_int_from_str_line(lines[1])
    c = parse_int_from_str_line(lines[2])

    assert a == mod.n1, f"expected={mod.n1} actual={a}"
    assert b == mod.n2, f"expected={mod.n2} actual={b}"
    assert c == mod.n1 + mod.n2, f"expected={mod.n1 + mod.n2} actual={c}"