import importlib.util
import pathlib
import re

import pytest


def _run_module_and_capture_output(capsys):
    path = pathlib.Path(__file__).resolve().parent / "06_listTraversalAndSum.py"
    spec = importlib.util.spec_from_file_location("assignment_06_listTraversalAndSum", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return module, out


def _parse_total_from_output(out: str):
    matches = re.findall(r"total:\s*(-?\d+)\s*", out)
    assert matches, f"expected vs actual: {True} vs {False}"
    return int(matches[-1])


def test_total_printed_value(capsys):
    _, out = _run_module_and_capture_output(capsys)
    actual = _parse_total_from_output(out)
    expected = 21
    assert actual == expected, f"expected vs actual: {expected} vs {actual}"


def test_total_variable_value(capsys):
    module, _ = _run_module_and_capture_output(capsys)
    assert hasattr(module, "total"), f"expected vs actual: {True} vs {hasattr(module, 'total')}"
    actual = module.total
    expected = 21
    assert actual == expected, f"expected vs actual: {expected} vs {actual}"


def test_nums_unchanged(capsys):
    module, _ = _run_module_and_capture_output(capsys)
    assert hasattr(module, "nums"), f"expected vs actual: {True} vs {hasattr(module, 'nums')}"
    actual = module.nums
    expected = [1, 2, 3, 4, 5, 6]
    assert actual == expected, f"expected vs actual: {expected} vs {actual}"


def test_print_format_contains_label(capsys):
    _, out = _run_module_and_capture_output(capsys)
    actual = "total:" in out
    expected = True
    assert actual == expected, f"expected vs actual: {expected} vs {actual}"