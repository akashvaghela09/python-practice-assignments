import sys
import importlib.util
from pathlib import Path


def _run_script(path: Path, capsys):
    if not path.exists():
        raise AssertionError(f"Missing assignment file: {path}")
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(spec.name, None)
    spec.loader.exec_module(module)
    return capsys.readouterr().out


def test_output_exact(capsys):
    script_path = Path(__file__).resolve().parent / "08_nestedLoopsCoordinates.py"
    actual = _run_script(script_path, capsys)
    expected = "(0,0)\n(0,1)\n(0,2)\n(1,0)\n(1,1)\n(1,2)\n"
    if actual != expected:
        raise AssertionError(f"expected output:\n{expected}\nactual output:\n{actual}")
