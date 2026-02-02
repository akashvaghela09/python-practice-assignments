import importlib.util
import io
import os
import runpy
import contextlib
import pytest

MODULE_FILE = "07_comparisonsAndArithmetic.py"


def _run_script():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(MODULE_FILE, run_name="__main__")
    return buf.getvalue()


def test_file_exists():
    assert os.path.exists(MODULE_FILE)


def test_runs_without_error():
    _run_script()


def test_prints_exactly_true():
    out = _run_script()
    expected = "True\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_has_no_blanks_left():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    assert "__" not in src, f"expected={False!r} actual={('__' in src)!r}"


def test_check_is_boolean_and_true():
    spec = importlib.util.spec_from_file_location("comparisons_arithmetic_mod", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    expected_type = bool
    actual_type = type(getattr(mod, "check", None))
    assert actual_type is expected_type, f"expected={expected_type!r} actual={actual_type!r}"
    expected_val = True
    actual_val = getattr(mod, "check", None)
    assert actual_val is expected_val, f"expected={expected_val!r} actual={actual_val!r}"


def test_x_and_y_are_numbers():
    spec = importlib.util.spec_from_file_location("comparisons_arithmetic_mod2", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)

    x = getattr(mod, "x", None)
    y = getattr(mod, "y", None)

    assert isinstance(x, (int, float)), f"expected={(int, float)!r} actual={type(x)!r}"
    assert isinstance(y, (int, float)), f"expected={(int, float)!r} actual={type(y)!r}"


def test_expression_matches_spec():
    spec = importlib.util.spec_from_file_location("comparisons_arithmetic_mod3", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)

    x = mod.x
    y = mod.y
    expected = x + 2 * 3 > y
    actual = mod.check
    assert actual == expected, f"expected={expected!r} actual={actual!r}"