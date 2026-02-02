import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(monkeypatch, capsys, inputs):
    script_path = Path(__file__).resolve().parent / "10_nestedLoopBreakOnMarker.py"
    if not script_path.exists():
        pytest.fail(f"expected output: (file exists)\nactual output: missing file {script_path.name}")

    it = iter(inputs)

    def fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    spec = importlib.util.spec_from_file_location("mod_10_nestedLoopBreakOnMarker", str(script_path))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except EOFError:
        pass

    return capsys.readouterr().out


def test_nested_breaks_and_total(monkeypatch, capsys):
    out = _run_script(monkeypatch, capsys, ["1 2 0 100", "5 5", "9 0 9", "END"])
    expected = "Total: 22\n"
    if out != expected:
        pytest.fail(f"expected output: {expected}actual output: {out}")
