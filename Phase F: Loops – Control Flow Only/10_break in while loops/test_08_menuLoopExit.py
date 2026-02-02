import builtins
import importlib.util
import sys
from pathlib import Path
import pytest


def run_module_with_inputs(monkeypatch, capsys, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr(builtins, "input", fake_input)

    path = Path(__file__).resolve().parent / "08_menuLoopExit.py"
    spec = importlib.util.spec_from_file_location("menuLoopExit_08", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["menuLoopExit_08"] = module
    spec.loader.exec_module(module)

    return capsys.readouterr().out


def test_menu_loop_inc_inc_dec_q(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, ["inc", "inc", "dec", "q"])
    expected = "Counter: 1\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_menu_loop_ignores_other_commands(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, ["noop", "inc", "bad", "dec", "q"])
    expected = "Counter: 0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_menu_loop_strips_whitespace(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, ["  inc  ", "\tdec", "  q  "])
    expected = "Counter: 0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_menu_loop_quits_immediately(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, ["q"])
    expected = "Counter: 0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_menu_loop_only_final_print(monkeypatch, capsys):
    out = run_module_with_inputs(monkeypatch, capsys, ["inc", "q"])
    lines = out.splitlines()
    expected_lines = 1
    assert len(lines) == expected_lines, f"expected={expected_lines!r} actual={len(lines)!r}"
    expected_last = "Counter: 1"
    assert lines[-1] == expected_last, f"expected={expected_last!r} actual={lines[-1]!r}"