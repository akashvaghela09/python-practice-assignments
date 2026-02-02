import importlib.util
import io
import os
import contextlib
import re
import pytest

MODULE_FILE = "05_convertStringsToNumbers.py"


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location("student_mod_05", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _parse_numbers_from_stdout(stdout):
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip() != ""]
    if len(lines) != 3:
        return lines, None, None, None
    vals = []
    for ln in lines:
        if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", ln):
            return lines, None, None, None
        vals.append(float(ln) if "." in ln else int(ln))
    return lines, vals[0], vals[1], vals[2]


def test_module_imports_and_prints_three_lines():
    assert os.path.exists(MODULE_FILE)
    mod, out = _run_module_capture_stdout()
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 3


def test_converted_values_and_total_are_correct():
    mod, out = _run_module_capture_stdout()
    lines, a_out, b_out, total_out = _parse_numbers_from_stdout(out)
    assert a_out is not None and b_out is not None and total_out is not None
    expected_a = int(getattr(mod, "s_int"))
    expected_b = float(getattr(mod, "s_float"))
    expected_total = expected_a + expected_b
    assert a_out == expected_a, f"expected={expected_a} actual={a_out}"
    assert b_out == expected_b, f"expected={expected_b} actual={b_out}"
    assert total_out == expected_total, f"expected={expected_total} actual={total_out}"


def test_variables_exist_and_have_correct_types_and_values():
    mod, _ = _run_module_capture_stdout()
    assert hasattr(mod, "a")
    assert hasattr(mod, "b")
    assert hasattr(mod, "total")

    expected_a = int(mod.s_int)
    expected_b = float(mod.s_float)
    expected_total = expected_a + expected_b

    assert isinstance(mod.a, int), f"expected={int} actual={type(mod.a)}"
    assert isinstance(mod.b, float), f"expected={float} actual={type(mod.b)}"
    assert isinstance(mod.total, float), f"expected={float} actual={type(mod.total)}"

    assert mod.a == expected_a, f"expected={expected_a} actual={mod.a}"
    assert mod.b == expected_b, f"expected={expected_b} actual={mod.b}"
    assert mod.total == expected_total, f"expected={expected_total} actual={mod.total}"


def test_total_matches_sum_of_a_and_b():
    mod, _ = _run_module_capture_stdout()
    expected = mod.a + mod.b
    assert mod.total == expected, f"expected={expected} actual={mod.total}"