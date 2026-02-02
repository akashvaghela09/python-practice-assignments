import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(monkeypatch, capsys, inputs):
    script_path = Path(__file__).resolve().parent / "08_menuLoopExit.py"
    if not script_path.exists():
        pytest.fail(f"expected output: (file exists)\nactual output: missing file {script_path.name}")

    it = iter(inputs)

    def fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    spec = importlib.util.spec_from_file_location("mod_08_menuLoopExit", str(script_path))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except EOFError:
        pass

    return capsys.readouterr().out


def test_menu_counter(monkeypatch, capsys):
    out = _run_script(monkeypatch, capsys, ["inc", "inc", "dec", "q"])
    expected = "Counter: 1\n"
    if out != expected:
        pytest.fail(f"expected output: {expected}actual output: {out}")
