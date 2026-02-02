import importlib.util
from pathlib import Path
import sys


def _run_module_capture_stdout(path: Path):
    if not path.exists():
        raise AssertionError(f"Assignment file does not exist: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load assignment module")

    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_stdout_exact():
    assignment_path = Path(__file__).resolve().parent / "04_validate_username_characters.py"
    actual = _run_module_capture_stdout(assignment_path)
    expected = "VALID\nINVALID\n"
    if actual != expected:
        raise AssertionError(f"expected output:\n{expected}\nactual output:\n{actual}")
