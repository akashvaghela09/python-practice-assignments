import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(path: Path, monkeypatch, inputs=None):
    if inputs is None:
        inputs = []
    it = iter(inputs)

    def _fake_input(prompt=None):
        try:
            return next(it)
        except StopIteration:
            raise RuntimeError("No more input")

    monkeypatch.setattr("builtins.input", _fake_input)

    captured = []

    def _fake_write(s):
        captured.append(s)
        return len(s)

    monkeypatch.setattr(sys.stdout, "write", _fake_write)

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return "".join(captured)


def test_output_exact_for_sample_input(monkeypatch):
    path = (Path(__file__).resolve().parent / "07_userInputVariables.py").resolve()
    if not path.exists():
        pytest.fail("Missing file: 07_userInputVariables.py")

    expected = "Mia will be 9 next year.\n"
    actual = _run_script(path, monkeypatch, inputs=["Mia", "8"])
    if actual != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{actual}")
