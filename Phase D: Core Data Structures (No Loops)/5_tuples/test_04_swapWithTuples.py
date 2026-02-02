import importlib.util
import os
import sys


def _run_module_capture_stdout(module_filename, monkeypatch):
    captured = []
    monkeypatch.setattr(sys, "stdout", type("S", (), {"write": lambda self, s: captured.append(s)})())
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = "".join(captured)
    lines = [line for line in out.splitlines() if line.strip() != ""]
    return module, lines


def test_swapped_values_in_namespace(monkeypatch):
    module, _ = _run_module_capture_stdout("04_swapWithTuples.py", monkeypatch)
    assert hasattr(module, "a")
    assert hasattr(module, "b")
    expected_a, expected_b = 9, 3
    actual_a, actual_b = module.a, module.b
    assert (actual_a, actual_b) == (expected_a, expected_b), f"expected={(expected_a, expected_b)} actual={(actual_a, actual_b)}"


def test_prints_two_lines_in_correct_order(monkeypatch):
    _, lines = _run_module_capture_stdout("04_swapWithTuples.py", monkeypatch)
    expected = ["9", "3"]
    actual = lines[:2]
    assert actual == expected, f"expected={expected} actual={actual}"
    assert len(lines) == 2, f"expected={2} actual={len(lines)}"