import sys
import importlib.util
from pathlib import Path

def _run_script(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing assignment file: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        spec.loader.exec_module(module)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

def test_output_exact():
    assignment_path = Path(__file__).resolve().parent / "09_nestedLoops_skipMarkedSeats.py"
    actual = _run_script(assignment_path)
    expected = "A1\nA2\nA4\nB1\nB2\nB3\nB4\nC1\nC3\nC4\n"
    if actual != expected:
        raise AssertionError(f"expected output:\n{expected}\nactual output:\n{actual}")
