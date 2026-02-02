import builtins
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


def _run_script_with_input(script_path, user_input: str):
    old_input = builtins.input
    try:
        builtins.input = lambda: user_input
        buf = io.StringIO()
        with redirect_stdout(buf):
            spec = importlib.util.spec_from_file_location("student_mod", script_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        return buf.getvalue()
    finally:
        builtins.input = old_input


def _expected_output(n: int) -> str:
    start = n if n % 2 == 0 else n - 1
    if start < 0:
        return ""
    lines = [str(x) for x in range(start, -1, -2)]
    return ("\n".join(lines) + "\n") if lines else ""


def test_even_input_counts_down():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "8\n")
    exp = _expected_output(8)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_odd_input_starts_at_prev_even():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "9\n")
    exp = _expected_output(9)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_zero_input_outputs_zero_only():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "0\n")
    exp = _expected_output(0)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_one_input_outputs_zero_only():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "1\n")
    exp = _expected_output(1)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_negative_input_outputs_nothing():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "-3\n")
    exp = _expected_output(-3)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_large_input_sequence_correct():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    n = 50
    out = _run_script_with_input(script, f"{n}\n")
    exp = _expected_output(n)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_ignores_surrounding_spaces_in_input():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    out = _run_script_with_input(script, "   6   \n")
    exp = _expected_output(6)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_outputs_only_evens_and_descending():
    script = os.path.join(os.path.dirname(__file__), "02_countDownByTwo.py")
    n = 17
    out = _run_script_with_input(script, f"{n}\n")
    exp = _expected_output(n)
    assert out == exp, f"expected={exp!r} actual={out!r}"