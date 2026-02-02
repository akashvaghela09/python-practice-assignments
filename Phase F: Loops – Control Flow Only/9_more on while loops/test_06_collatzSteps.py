import importlib.util
import sys
import io
import pathlib
import builtins
import pytest

MODULE_NAME = "06_collatzSteps"
FILE_PATH = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"


def _run_with_input(inp: str):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(FILE_PATH))
    module = importlib.util.module_from_spec(spec)

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(module)
        out = sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected single line vs actual lines={lines}"
    try:
        val = int(lines[0])
    except Exception:
        assert False, f"expected int vs actual output={lines[0]!r}"
    return val


def _collatz_steps(n: int) -> int:
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


@pytest.mark.parametrize(
    "n",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 25, 27, 97],
)
def test_collatz_steps_values(n):
    expected = _collatz_steps(n)
    actual = _run_with_input(f"{n}\n")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_collatz_steps_large_even():
    n = 10**6
    expected = _collatz_steps(n)
    actual = _run_with_input(f"{n}\n")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_collatz_steps_large_odd():
    n = 999_999
    expected = _collatz_steps(n)
    actual = _run_with_input(f"{n}\n")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_input_stripping_and_newline_variants():
    n = 6
    expected = _collatz_steps(n)
    actual = _run_with_input("   6   \n")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_does_not_use_input_more_than_once(monkeypatch):
    calls = {"count": 0}

    def fake_input(prompt=None):
        calls["count"] += 1
        if calls["count"] > 1:
            raise AssertionError("input called more than once")
        return "6"

    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(FILE_PATH))
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    monkeypatch.setattr(builtins, "input", fake_input)
    try:
        spec.loader.exec_module(module)
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected single line vs actual lines={lines}"
    expected = _collatz_steps(6)
    actual = int(lines[0])
    assert actual == expected, f"expected={expected} actual={actual}"