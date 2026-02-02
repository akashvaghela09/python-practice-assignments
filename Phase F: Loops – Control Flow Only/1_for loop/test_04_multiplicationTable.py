import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(path: Path):
    if not path.exists():
        pytest.fail(f"Missing assignment file: {path}")

    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO
        sys.stdout = StringIO()
        spec.loader.exec_module(module)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    return output


def test_multiplication_table_exact_stdout():
    script_path = Path(__file__).resolve().parent / "04_multiplicationTable.py"
    out = _run_script(script_path)
    expected = "7 x 1 = 7\n7 x 2 = 14\n7 x 3 = 21\n7 x 4 = 28\n7 x 5 = 35\n"
    if out != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{out}")
