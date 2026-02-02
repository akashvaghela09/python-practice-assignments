import sys
import importlib.util
from pathlib import Path
import pytest

from io import StringIO

def _run_script(input_data: str):
    script_path = Path(__file__).resolve().parent / "10_menuLoopCalculator.py"
    if not script_path.exists():
        pytest.fail(f"expected output:\n<file exists>\nactual output:\n{script_path.name} not found")

    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()

    spec = importlib.util.spec_from_file_location("mod_10_menuLoopCalculator", str(script_path))
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


def test_menu_example_interaction():
    input_data = "add\n2\n3\nsub\n10\n4\ndiv\n5\n0\nquit\n"
    actual = _run_script(input_data)
    expected = "5.0\n6.0\nCannot divide by zero\nBye\n"
    _assert_exact(actual, expected)


def test_menu_mul_then_quit():
    input_data = "mul\n2\n4\nquit\n"
    actual = _run_script(input_data)
    expected = "8.0\nBye\n"
    _assert_exact(actual, expected)


def test_menu_quit_immediately():
    input_data = "quit\n"
    actual = _run_script(input_data)
    expected = "Bye\n"
    _assert_exact(actual, expected)
