import subprocess
import sys
import os
import pytest

MODULE_FILENAME = "06_printCustomSeparator.py"


def _run_script():
    script_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    proc = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )
    return proc


def test_runs_without_error():
    proc = _run_script()
    assert proc.returncode == 0, f"expected=0 actual={proc.returncode}"


def test_stdout_exact():
    proc = _run_script()
    expected = "1 | 2 | 3\n"
    actual = proc.stdout
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_stderr_empty():
    proc = _run_script()
    expected = ""
    actual = proc.stderr
    assert actual == expected, f"expected={expected!r} actual={actual!r}"