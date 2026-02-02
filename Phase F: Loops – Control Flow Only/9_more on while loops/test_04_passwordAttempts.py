import sys
import importlib.util
from pathlib import Path
import pytest

from io import StringIO

def _run_script(input_data: str):
    script_path = Path(__file__).resolve().parent / "04_passwordAttempts.py"
    if not script_path.exists():
        pytest.fail(f"expected output:\n<file exists>\nactual output:\n{script_path.name} not found")

    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()

    spec = importlib.util.spec_from_file_location("mod_04_passwordAttempts", str(script_path))
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


def test_password_granted_first_try():
    actual = _run_script("opensesame\n")
    expected = "Access granted\n"
    _assert_exact(actual, expected)


def test_password_granted_third_try():
    actual = _run_script("nope\nwrong\nopensesame\n")
    expected = "Access granted\n"
    _assert_exact(actual, expected)


def test_password_denied_after_three():
    actual = _run_script("a\nb\nc\n")
    expected = "Access denied\n"
    _assert_exact(actual, expected)
