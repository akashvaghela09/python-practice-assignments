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
    script_path = Path(__file__).resolve().parent / "10_traceLoopState.py"
    actual = _run_script(script_path, capsys)
    expected = "i=0 before=1 after=1\ni=1 before=1 after=2\ni=2 before=2 after=6\ni=3 before=6 after=24\nfinal: 24\n"
    if actual != expected:
        raise AssertionError(f"expected output:\n{expected}\nactual output:\n{actual}")
