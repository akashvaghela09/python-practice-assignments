import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(monkeypatch, capsys, inputs):
    script_path = Path(__file__).resolve().parent / "02_findFirstNegative.py"
    if not script_path.exists():
        pytest.fail(f"expected output: (file exists)\nactual output: missing file {script_path.name}")

    it = iter(inputs)

    def fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    spec = importlib.util.spec_from_file_location("mod_02_findFirstNegative", str(script_path))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except EOFError:
        pass

    return capsys.readouterr().out


def test_first_negative_breaks_immediately(monkeypatch, capsys):
    out = _run_script(monkeypatch, capsys, ["4", "2", "-7", "9"])
    expected = "First negative: -7\n"
    if out != expected:
        pytest.fail(f"expected output: {expected}actual output: {out}")
