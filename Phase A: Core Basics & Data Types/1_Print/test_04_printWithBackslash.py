import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("04_printWithBackslash.py")


def run_script():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_script_runs_successfully():
    code, out, err = run_script()
    assert code == 0, f"expected=0 actual={code}"


def test_no_stderr_output():
    code, out, err = run_script()
    assert err == "", f"expected='' actual={err!r}"


def test_prints_exact_windows_path():
    code, out, err = run_script()
    expected = "C:\\Users\\Ava\\Documents\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_single_line_only():
    code, out, err = run_script()
    expected_lines = ["C:\\Users\\Ava\\Documents"]
    actual_lines = out.splitlines()
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"