import importlib.util
import os
import sys


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_10", path)
    mod = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    try:
        from io import StringIO

        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(mod)
        return buf.getvalue(), mod
    finally:
        sys.stdout = old_stdout


def test_prints_first_prime_only(capsys):
    path = os.path.join(os.path.dirname(__file__), "10_nestedBreakUsingFlagFirstPrime.py")
    out, _ = _run_script_capture_stdout(path)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1
    assert lines[0].isdigit()
    val = int(lines[0])
    assert val >= 2
    for d in range(2, val):
        assert val % d != 0


def test_prime_printed_is_from_list_and_is_first_prime(capsys):
    path = os.path.join(os.path.dirname(__file__), "10_nestedBreakUsingFlagFirstPrime.py")
    out, mod = _run_script_capture_stdout(path)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1
    assert hasattr(mod, "nums")
    nums = list(mod.nums)
    printed = int(lines[0])

    assert printed in nums

    def is_prime(n):
        if n < 2:
            return False
        for d in range(2, n):
            if n % d == 0:
                return False
        return True

    expected_first = None
    for n in nums:
        if is_prime(n):
            expected_first = n
            break

    assert expected_first is not None
    assert printed == expected_first


def test_no_extra_output_or_non_numeric(capsys):
    path = os.path.join(os.path.dirname(__file__), "10_nestedBreakUsingFlagFirstPrime.py")
    out, _ = _run_script_capture_stdout(path)
    stripped = out.strip()
    assert stripped != ""
    parts = stripped.split()
    assert len(parts) == 1
    assert parts[0].lstrip("+-").isdigit()