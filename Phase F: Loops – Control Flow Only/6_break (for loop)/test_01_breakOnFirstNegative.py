import sys
import importlib.util
from pathlib import Path
import pytest

def _run_script(script_path: Path):
    if not script_path.exists():
        raise FileNotFoundError(f"Missing assignment file: {script_path}")

    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)


def test_output_exact(capsys):
    script_path = Path(__file__).resolve().parent / "01_breakOnFirstNegative.py"
    _run_script(script_path)
    actual = capsys.readouterr().out
    expected = "4\n2\n7\n"
    assert actual == expected, f"expected output:\n{expected}\nactual output:\n{actual}"
