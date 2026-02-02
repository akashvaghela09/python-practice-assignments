import builtins
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

FILE_NAME = "08_primeCheckWhile.py"


def run_program_with_input(inp: str) -> str:
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("primecheck_module", path)
    module = importlib.util.module_from_spec(spec)

    old_input = builtins.input
    builtins.input = lambda: inp

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            spec.loader.exec_module(module)
    finally:
        builtins.input = old_input

    return buf.getvalue().strip()


def assert_output(n: int, expected: str):
    actual = run_program_with_input(f"{n}\n")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_small_cases_not_prime():
    assert_output(0, "Not prime")
    assert_output(1, "Not prime")


def test_two_is_prime():
    assert_output(2, "Prime")


def test_three_is_prime():
    assert_output(3, "Prime")


def test_four_not_prime():
    assert_output(4, "Not prime")


def test_nine_not_prime():
    assert_output(9, "Not prime")


def test_perfect_square_not_prime():
    assert_output(49, "Not prime")


def test_large_prime():
    assert_output(97, "Prime")


def test_large_composite():
    assert_output(221, "Not prime")


def test_even_greater_than_two_not_prime():
    assert_output(100, "Not prime")