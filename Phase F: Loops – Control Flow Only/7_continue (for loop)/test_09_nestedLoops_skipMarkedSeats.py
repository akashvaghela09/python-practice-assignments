import importlib
import sys
import types
import pytest


MODULE_NAME = "09_nestedLoops_skipMarkedSeats"


def run_module_and_capture_output(monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    importlib.import_module(MODULE_NAME)
    out = "".join(captured)
    return out


def test_output_matches_expected_lines(monkeypatch):
    out = run_module_and_capture_output(monkeypatch)

    rows = ["A", "B", "C"]
    cols = [1, 2, 3, 4]
    blocked = {"A3", "C2"}
    expected_lines = [f"{r}{c}" for r in rows for c in cols if f"{r}{c}" not in blocked]
    expected = "\n".join(expected_lines) + ("\n" if expected_lines else "")

    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_does_not_print_blocked_seats(monkeypatch):
    out = run_module_and_capture_output(monkeypatch)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    blocked = {"A3", "C2"}
    actual_blocked = [s for s in blocked if s in lines]
    assert actual_blocked == [], f"expected={[]} actual={actual_blocked}"


def test_prints_all_unblocked_unique_and_correct_count(monkeypatch):
    out = run_module_and_capture_output(monkeypatch)
    lines = out.splitlines()

    rows = ["A", "B", "C"]
    cols = [1, 2, 3, 4]
    blocked = {"A3", "C2"}
    expected_lines = [f"{r}{c}" for r in rows for c in cols if f"{r}{c}" not in blocked]

    assert len(lines) == len(expected_lines), f"expected={len(expected_lines)!r} actual={len(lines)!r}"
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"
    assert len(set(lines)) == len(lines), f"expected={len(lines)!r} actual={len(set(lines))!r}"


def test_prints_each_seat_on_its_own_line(monkeypatch):
    out = run_module_and_capture_output(monkeypatch)
    rows = ["A", "B", "C"]
    cols = [1, 2, 3, 4]
    blocked = {"A3", "C2"}
    expected_lines = [f"{r}{c}" for r in rows for c in cols if f"{r}{c}" not in blocked]

    expected_newlines = len(expected_lines)
    actual_newlines = out.count("\n")
    assert actual_newlines == expected_newlines, f"expected={expected_newlines!r} actual={actual_newlines!r}"