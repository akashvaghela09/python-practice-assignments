import ast
import importlib.util
import pathlib
import re
import subprocess
import sys


FILE_NAME = "08_sumOfSquares.py"


def _run_script_with_input(inp: str):
    p = subprocess.run(
        [sys.executable, FILE_NAME],
        input=inp,
        text=True,
        capture_output=True,
        cwd=pathlib.Path(__file__).resolve().parent,
    )
    return p.returncode, p.stdout, p.stderr


def _expected_sum_squares(n: int) -> int:
    return sum(k * k for k in range(1, n + 1))


def test_no_blanks_left_in_source():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    assert "____" not in src


def test_program_parses_as_python():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    ast.parse(src)


def test_import_has_no_side_effects(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda: "0")
    spec = importlib.util.spec_from_file_location("mod08", FILE_NAME)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    assert out.strip() == str(_expected_sum_squares(0))


def test_n_0():
    n = 0
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    got = out.strip()
    exp = str(_expected_sum_squares(n))
    assert got == exp, f"expected={exp} actual={got}"


def test_n_1():
    n = 1
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    got = out.strip()
    exp = str(_expected_sum_squares(n))
    assert got == exp, f"expected={exp} actual={got}"


def test_n_3_example():
    n = 3
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    got = out.strip()
    exp = str(_expected_sum_squares(n))
    assert got == exp, f"expected={exp} actual={got}"


def test_n_10():
    n = 10
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    got = out.strip()
    exp = str(_expected_sum_squares(n))
    assert got == exp, f"expected={exp} actual={got}"


def test_n_50():
    n = 50
    rc, out, err = _run_script_with_input(f"{n}\n")
    assert rc == 0
    got = out.strip()
    exp = str(_expected_sum_squares(n))
    assert got == exp, f"expected={exp} actual={got}"


def test_rejects_non_integer_input_gracefully():
    rc, out, err = _run_script_with_input("abc\n")
    assert rc != 0
    assert (out.strip() == "") or re.fullmatch(r"\s*", out) is not None