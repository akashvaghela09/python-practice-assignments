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


def test_print_numbers_exact_stdout():
    script_path = Path(__file__).resolve().parent / "01_printNumbers.py"
    out = _run_script(script_path)
    expected = "1\n2\n3\n4\n5\n"
    if out != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{out}")
