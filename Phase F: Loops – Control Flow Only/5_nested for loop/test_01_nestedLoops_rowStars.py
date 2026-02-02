import importlib
import io
import os
import sys
import types
import pytest


MODULE_NAME = "01_nestedLoops_rowStars"


def run_module_capture_stdout():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        importlib.import_module(MODULE_NAME)
    finally:
        sys.stdout = old
    return buf.getvalue()


def parse_lines(output):
    s = output.rstrip("\n")
    if s == "":
        return []
    return s.splitlines()


def test_prints_expected_grid_exact_stdout():
    out = run_module_capture_stdout()
    expected = "*****\n*****\n*****\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_module_result_variable_matches_expected():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    mod = importlib.import_module(MODULE_NAME)
    assert hasattr(mod, "result")
    expected = "*****\n*****\n*****"
    actual = getattr(mod, "result")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_module_output_lines_structure():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    mod = importlib.import_module(MODULE_NAME)
    assert hasattr(mod, "output_lines")
    actual = getattr(mod, "output_lines")
    expected = ["*****", "*****", "*****"]
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_stdout_has_three_lines_each_five_stars_only():
    out = run_module_capture_stdout()
    lines = parse_lines(out)
    expected_lines_count = 3
    actual_lines_count = len(lines)
    assert actual_lines_count == expected_lines_count, f"expected={expected_lines_count!r} actual={actual_lines_count!r}"
    for line in lines:
        expected_len = 5
        actual_len = len(line)
        assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"
        expected_set = {"*"}
        actual_set = set(line)
        assert actual_set == expected_set, f"expected={expected_set!r} actual={actual_set!r}"


def test_uses_nested_for_loops_in_source():
    path = os.path.join(os.path.dirname(__file__), f"{MODULE_NAME}.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    for_count = src.count("for ")
    expected_min = 2
    actual = for_count
    assert actual >= expected_min, f"expected={expected_min!r} actual={actual!r}"