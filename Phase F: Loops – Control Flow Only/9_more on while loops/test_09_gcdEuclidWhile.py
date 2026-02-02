import importlib.util
import os
import sys
import subprocess
import textwrap
import pytest

SCRIPT_NAME = "09_gcdEuclidWhile.py"


def _run_script_with_input(inp: str):
    proc = subprocess.run(
        [sys.executable, SCRIPT_NAME],
        input=inp,
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _expected_gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def _parse_int_output(out: str) -> int:
    s = out.strip()
    if not s:
        raise AssertionError("missing output")
    parts = s.split()
    if len(parts) != 1:
        raise AssertionError("unexpected output format")
    return int(parts[0])


def test_script_exists():
    assert os.path.exists(SCRIPT_NAME)


@pytest.mark.parametrize(
    "a,b",
    [
        (54, 24),
        (24, 54),
        (0, 0),
        (0, 7),
        (7, 0),
        (-54, 24),
        (54, -24),
        (-54, -24),
        (270, 192),
        (1, 1),
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ],
)
def test_gcd_various_inputs(a, b):
    rc, out, err = _run_script_with_input(f"{a}\n{b}\n")
    assert rc == 0, f"expected={0} actual={rc}"
    actual = _parse_int_output(out)
    expected = _expected_gcd(a, b)
    assert actual == expected, f"expected={expected} actual={actual}"
    assert actual >= 0, f"expected={True} actual={actual >= 0}"


def test_gcd_coprime():
    a, b = 35, 64
    rc, out, err = _run_script_with_input(f"{a}\n{b}\n")
    assert rc == 0, f"expected={0} actual={rc}"
    actual = _parse_int_output(out)
    expected = _expected_gcd(a, b)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_gcd_with_large_values():
    a, b = 1234567890, 987654321
    rc, out, err = _run_script_with_input(f"{a}\n{b}\n")
    assert rc == 0, f"expected={0} actual={rc}"
    actual = _parse_int_output(out)
    expected = _expected_gcd(a, b)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_output_is_single_integer_only():
    a, b = 48, 18
    rc, out, err = _run_script_with_input(f"{a}\n{b}\n")
    assert rc == 0, f"expected={0} actual={rc}"
    stripped = out.strip()
    assert stripped == str(_parse_int_output(out)), f"expected={str(_parse_int_output(out))} actual={stripped}"


def test_rejects_non_integer_input_gracefully_by_error_code():
    rc, out, err = _run_script_with_input("abc\n5\n")
    assert rc != 0, f"expected={False} actual={rc == 0}"