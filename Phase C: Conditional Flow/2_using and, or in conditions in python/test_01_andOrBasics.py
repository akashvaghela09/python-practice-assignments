import sys
import importlib.util
from pathlib import Path

def _run_module(path: Path):
    if not path.exists():
        raise AssertionError(f"Assignment file does not exist: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)  # type: ignore
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_output_in_range():
    assignment_path = Path(__file__).resolve().parent / "01_andOrBasics.py"
    out = _run_module(assignment_path)
    expected = "IN RANGE\n"
    assert out == expected, f"expected output:\n{expected}\nactual output:\n{out}"
