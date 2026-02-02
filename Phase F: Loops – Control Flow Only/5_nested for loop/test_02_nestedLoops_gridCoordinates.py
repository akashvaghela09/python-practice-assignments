import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(path: Path):
    if not path.exists():
        pytest.fail(f"Missing assignment file: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        pytest.fail(f"Could not load assignment file: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_grid_coordinates_stdout_exact(capsys):
    script_path = Path(__file__).resolve().parent / "02_nestedLoops_gridCoordinates.py"
    _run_script(script_path)

    captured = capsys.readouterr()
    expected = "(0,0) (1,0) (2,0)\n(0,1) (1,1) (2,1)\n"
    actual = captured.out
    if actual != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{actual}")
    if captured.err != "":
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{actual}")
