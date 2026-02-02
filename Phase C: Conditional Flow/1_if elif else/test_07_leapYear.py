import importlib.util
import pathlib
import sys
import types
import pytest


MODULE_NAME = "07_leapYear"
FILE_NAME = "07_leapYear.py"


def _load_module_fresh(monkeypatch):
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    if not path.exists():
        path = pathlib.Path(FILE_NAME).resolve()
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, MODULE_NAME, module)
    spec.loader.exec_module(module)
    return module


def _run_with_year(monkeypatch, capsys, year_value):
    module = _load_module_fresh(monkeypatch)
    monkeypatch.setattr(module, "year", year_value, raising=False)
    code = pathlib.Path(module.__file__).read_text(encoding="utf-8")
    exec(compile(code, module.__file__, "exec"), module.__dict__)
    out = capsys.readouterr().out
    return out


def _assert_single_line_output(out):
    assert out is not None
    stripped = out.strip("\n")
    lines = [ln for ln in stripped.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected={1} actual={len(lines)}"
    return lines[0].strip()


def test_prints_only_leap_or_not_leap(monkeypatch, capsys):
    out = _run_with_year(monkeypatch, capsys, 2000)
    line = _assert_single_line_output(out)
    assert line in {"Leap", "Not Leap"}, f"expected={'Leap|Not Leap'} actual={line}"


@pytest.mark.parametrize(
    "year_value, expected",
    [
        (2000, "Leap"),
        (1900, "Not Leap"),
        (1996, "Leap"),
        (1999, "Not Leap"),
        (2400, "Leap"),
        (2100, "Not Leap"),
        (2004, "Leap"),
        (2001, "Not Leap"),
    ],
)
def test_leap_year_rules(monkeypatch, capsys, year_value, expected):
    out = _run_with_year(monkeypatch, capsys, year_value)
    line = _assert_single_line_output(out)
    assert line == expected, f"expected={expected} actual={line}"


def test_respects_year_variable_not_hardcoded(monkeypatch, capsys):
    out1 = _run_with_year(monkeypatch, capsys, 2000)
    out2 = _run_with_year(monkeypatch, capsys, 1900)
    line1 = _assert_single_line_output(out1)
    line2 = _assert_single_line_output(out2)
    assert line1 != line2, f"expected={'different'} actual={(line1, line2)}"