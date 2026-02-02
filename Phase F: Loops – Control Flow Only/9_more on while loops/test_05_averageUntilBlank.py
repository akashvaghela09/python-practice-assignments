import sys
import importlib.util
from pathlib import Path
import pytest

from io import StringIO

def _run_script(input_data: str):
    script_path = Path(__file__).resolve().parent / "05_averageUntilBlank.py"
    if not script_path.exists():
        pytest.fail(f"expected output:\n<file exists>\nactual output:\n{script_path.name} not found")

    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()

    spec = importlib.util.spec_from_file_location("mod_05_averageUntilBlank", str(script_path))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        out = sys.stdout.getvalue()
        sys.stdin, sys.stdout = old_stdin, old_stdout
    return out


def _assert_exact(actual: str, expected: str):
    if actual != expected:
        pytest.fail(f"expected output:\n{expected}\nactual output:\n{actual}")


def test_average_example():
    actual = _run_script("3\n4\n3\n\n")
    expected = "3.33\n"
    _assert_exact(actual, expected)


def test_average_single_value():
    actual = _run_script("2.5\n\n")
    expected = "2.50\n"
    _assert_exact(actual, expected)


def test_average_no_data():
    actual = _run_script("\n")
    expected = "No data\n"
    _assert_exact(actual, expected)
