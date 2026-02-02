import sys
import importlib.util
from pathlib import Path
import pytest

from io import StringIO

def _run_script(input_data: str):
    script_path = Path(__file__).resolve().parent / "09_gcdEuclidWhile.py"
    if not script_path.exists():
        pytest.fail(f"expected output:\n<file exists>\nactual output:\n{script_path.name} not found")

    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()

    spec = importlib.util.spec_from_file_location("mod_09_gcdEuclidWhile", str(script_path))
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


def test_gcd_example():
    actual = _run_script("54\n24\n")
    expected = "6\n"
    _assert_exact(actual, expected)


def test_gcd_with_negatives():
    actual = _run_script("-54\n24\n")
    expected = "6\n"
    _assert_exact(actual, expected)


def test_gcd_with_zero():
    actual = _run_script("0\n5\n")
    expected = "5\n"
    _assert_exact(actual, expected)
