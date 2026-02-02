import importlib.util
import os
import sys
import re
import pytest

MODULE_FILENAME = "10_truthTableGenerator.py"


def _load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_module_capture_output(capsys):
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    module_name = f"_assignment_{os.path.splitext(MODULE_FILENAME)[0]}"
    if module_name in sys.modules:
        del sys.modules[module_name]
    _load_module_from_path(path, module_name)
    out = capsys.readouterr().out
    return out


def _expected_lines():
    pairs = [(False, False), (False, True), (True, False), (True, True)]
    lines = []
    for A, B in pairs:
        result = (A and (not B)) or ((not A) and B)
        lines.append(f"A={A} B={B} => {result}")
    return lines


def test_syntax_is_valid():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    compile(src, MODULE_FILENAME, "exec")


def test_prints_four_lines_exact(capsys):
    out = _run_module_capture_output(capsys)
    lines = out.splitlines()
    exp = _expected_lines()
    assert len(lines) == len(exp), f"expected={len(exp)} actual={len(lines)}"
    assert lines == exp, f"expected={exp} actual={lines}"


def test_line_formatting_matches_required_pattern(capsys):
    out = _run_module_capture_output(capsys)
    lines = out.splitlines()
    pattern = re.compile(r"^A=(True|False) B=(True|False) => (True|False)$")
    mismatches = [ln for ln in lines if not pattern.match(ln)]
    assert mismatches == [], f"expected=[] actual={mismatches}"


def test_order_of_pairs_is_correct(capsys):
    out = _run_module_capture_output(capsys)
    lines = out.splitlines()
    exp_pairs = ["A=False B=False", "A=False B=True", "A=True B=False", "A=True B=True"]
    actual_pairs = [ln.split(" => ")[0] if " => " in ln else ln for ln in lines]
    assert actual_pairs == exp_pairs, f"expected={exp_pairs} actual={actual_pairs}"


def test_xor_truth_values(capsys):
    out = _run_module_capture_output(capsys)
    lines = out.splitlines()
    exp = _expected_lines()
    actual_results = [ln.split(" => ")[1] if " => " in ln else None for ln in lines]
    expected_results = [ln.split(" => ")[1] for ln in exp]
    assert actual_results == expected_results, f"expected={expected_results} actual={actual_results}"