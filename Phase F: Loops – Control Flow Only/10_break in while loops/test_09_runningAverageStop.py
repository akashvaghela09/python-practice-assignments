import builtins
import importlib.util
import io
import os
import sys
import types
import pytest


FILE_NAME = "09_runningAverageStop.py"


def _run_script_with_inputs(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    captured = io.StringIO()
    old = sys.stdout
    sys.stdout = captured
    try:
        spec = importlib.util.spec_from_file_location("mod09_runningAverageStop", os.path.abspath(FILE_NAME))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return captured.getvalue()


def _parse_last_average_line(output):
    lines = [ln.rstrip("\n") for ln in output.splitlines() if ln.strip() != ""]
    assert lines, f"expected output lines vs actual: {1} vs {0}"
    return lines[-1]


@pytest.mark.parametrize(
    "inputs,expected_line",
    [
        (["10", "20", "30", "done"], "Average: 20.00"),
        (["5", "done"], "Average: 5.00"),
        (["1", "2", "done"], "Average: 1.50"),
        (["-10", "10", "done"], "Average: 0.00"),
    ],
)
def test_running_average_outputs_expected(monkeypatch, inputs, expected_line):
    out = _run_script_with_inputs(monkeypatch, inputs)
    last = _parse_last_average_line(out)
    assert last == expected_line, f"expected vs actual: {expected_line!r} vs {last!r}"


def test_exactly_two_decimals(monkeypatch):
    out = _run_script_with_inputs(monkeypatch, ["1", "2", "3", "done"])
    last = _parse_last_average_line(out)
    assert last.startswith("Average: "), f"expected vs actual: {'Average: '!r} vs {last[:9]!r}"
    value = last.split("Average: ", 1)[1].strip()
    assert value.count(".") == 1, f"expected vs actual: {1} vs {value.count('.')}"
    frac = value.split(".", 1)[1]
    assert len(frac) == 2, f"expected vs actual: {2} vs {len(frac)}"


def test_stops_at_done_and_ignores_following_inputs(monkeypatch):
    out = _run_script_with_inputs(monkeypatch, ["10", "done", "999", "1000"])
    last = _parse_last_average_line(out)
    assert last == "Average: 10.00", f"expected vs actual: {'Average: 10.00'!r} vs {last!r}"


def test_no_extra_nonempty_lines(monkeypatch):
    out = _run_script_with_inputs(monkeypatch, ["10", "20", "done"])
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected vs actual: {1} vs {len(lines)}"
    assert lines[0].startswith("Average: "), f"expected vs actual: {'Average: '!r} vs {lines[0][:8]!r}"