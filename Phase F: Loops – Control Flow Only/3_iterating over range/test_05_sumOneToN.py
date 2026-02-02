import os
import re
import sys
import subprocess
import importlib.util
import pathlib
import pytest


FILE_NAME = "05_sumOneToN.py"


def _run_script_with_input(inp: str):
    p = subprocess.run(
        [sys.executable, FILE_NAME],
        input=inp,
        text=True,
        capture_output=True,
        cwd=os.getcwd(),
    )
    return p.returncode, p.stdout, p.stderr


def _expected_sum(n: int) -> int:
    return n * (n + 1) // 2


def test_no_placeholders_left():
    path = pathlib.Path(FILE_NAME)
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "____" not in content


@pytest.mark.parametrize("n", [0, 1, 2, 4, 10, 25, 100])
def test_outputs_correct_sum(n):
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    actual_s = out.strip()
    expected_s = str(_expected_sum(n))
    assert actual_s == expected_s, f"expected={expected_s} actual={actual_s}"


def test_whitespace_tolerant_output():
    rc, out, err = _run_script_with_input("4\n")
    assert rc == 0
    expected_s = str(_expected_sum(4))
    actual_s = out.strip()
    assert actual_s == expected_s, f"expected={expected_s} actual={actual_s}"


def test_import_does_not_crash(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "3")
    spec = importlib.util.spec_from_file_location("sum_module_05", FILE_NAME)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "total")


def test_negative_n_expected_behavior_matches_loop():
    n = -5
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    actual_s = out.strip()
    expected_s = str(0)
    assert actual_s == expected_s, f"expected={expected_s} actual={actual_s}"