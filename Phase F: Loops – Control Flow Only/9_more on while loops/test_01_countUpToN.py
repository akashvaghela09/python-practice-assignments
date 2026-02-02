import sys
import importlib.util
from pathlib import Path
import pytest

def _run_script(input_data: str):
    script_path = Path(__file__).resolve().parent / "01_countUpToN.py"
    if not script_path.exists():
        pytest.fail(f"expected output:\n<file exists>\nactual output:\n{script_path.name} not found")

    old_stdin, old_stdout = sys.stdin, sys.stdout
    try:
        sys.stdin = type("_In", (), {"read": lambda self=-1: input_data, "readline": lambda self=-1: input_data.splitlines(True).pop(0) if False else ""})()
    except Exception:
        pass

    from io import StringIO
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()

    spec = importlib.util.spec_from_file_location("mod_01_countUpToN", str(script_path))
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


def test_count_up_basic():
    actual = _run_script("3\n")
    expected = "1\n2\n3\n"
    _assert_exact(actual, expected)


def test_count_up_one():
    actual = _run_script("1\n")
    expected = "1\n"
    _assert_exact(actual, expected)


def test_count_up_zero_prints_nothing():
    actual = _run_script("0\n")
    expected = ""
    _assert_exact(actual, expected)
