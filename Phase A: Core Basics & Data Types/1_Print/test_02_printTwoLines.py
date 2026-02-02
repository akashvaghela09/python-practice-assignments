import subprocess
import sys
from pathlib import Path

EXPECTED = "Line 1\nLine 2\n"


def _run_script(path: Path):
    proc = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_program_runs_without_error():
    path = Path(__file__).resolve().parent / "02_printTwoLines.py"
    code, out, err = _run_script(path)
    assert code == 0, f"expected=0 actual={code}\nstderr={err}"


def test_prints_exact_two_lines_in_order():
    path = Path(__file__).resolve().parent / "02_printTwoLines.py"
    code, out, err = _run_script(path)
    assert code == 0, f"expected=0 actual={code}\nstderr={err}"
    assert out == EXPECTED, f"expected={EXPECTED!r} actual={out!r}"