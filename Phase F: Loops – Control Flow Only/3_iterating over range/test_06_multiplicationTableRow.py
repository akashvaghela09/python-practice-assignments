import importlib.util
import sys
from pathlib import Path
import pytest


MODULE_FILE = "06_multiplicationTableRow.py"


def run_module_with_input(monkeypatch, capsys, inp: str):
    monkeypatch.setattr(sys, "stdin", type("S", (), {"readline": lambda self=None: inp})())
    spec = importlib.util.spec_from_file_location("student_mod", Path(MODULE_FILE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return out


@pytest.mark.parametrize("x", [0, 1, 3, -2, 7, 10])
def test_multiplication_table_exact(monkeypatch, capsys, x):
    out = run_module_with_input(monkeypatch, capsys, f"{x}\n")
    lines = out.splitlines()

    assert len(lines) == 10, f"expected=10 actual={len(lines)}"

    expected = [f"{x} * {i} = {x*i}" for i in range(1, 11)]
    for idx, (got, exp) in enumerate(zip(lines, expected), start=1):
        assert got == exp, f"expected={exp!r} actual={got!r}"


def test_no_extra_whitespace_in_lines(monkeypatch, capsys):
    x = 4
    out = run_module_with_input(monkeypatch, capsys, f"{x}\n")
    lines = out.splitlines()
    expected = [f"{x} * {i} = {x*i}" for i in range(1, 11)]

    assert len(lines) == 10, f"expected=10 actual={len(lines)}"
    for got, exp in zip(lines, expected):
        assert got == got.strip(), f"expected={got.strip()!r} actual={got!r}"
        assert got == exp, f"expected={exp!r} actual={got!r}"


def test_accepts_whitespace_around_input(monkeypatch, capsys):
    x = 6
    out = run_module_with_input(monkeypatch, capsys, f"   {x}   \n")
    lines = out.splitlines()
    expected = [f"{x} * {i} = {x*i}" for i in range(1, 11)]
    assert lines == expected, f"expected={expected!r} actual={lines!r}"


def test_output_ends_with_newline(monkeypatch, capsys):
    x = 2
    out = run_module_with_input(monkeypatch, capsys, f"{x}\n")
    assert out.endswith("\n"), f"expected={'\\n'!r} actual={out[-1:]!r}"