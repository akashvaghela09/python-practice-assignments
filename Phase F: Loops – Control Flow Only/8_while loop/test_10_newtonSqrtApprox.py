import importlib.util
import math
import os
import re
import sys
from pathlib import Path


def _load_module_from_file(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_file_parses_and_runs_without_syntax_error(capsys):
    file_path = Path(__file__).resolve().parent / "10_newtonSqrtApprox.py"
    assert file_path.exists()

    try:
        _load_module_from_file("newton_sqrt_approx_mod_run", file_path)
    except SyntaxError as e:
        assert False, f"expected=valid_python actual=SyntaxError:{e.msg}"

    out = capsys.readouterr().out
    assert "Approx sqrt:" in out, f"expected=output_contains_label actual={out!r}"


def test_output_format_and_value_close_to_math_sqrt(capsys):
    file_path = Path(__file__).resolve().parent / "10_newtonSqrtApprox.py"
    mod = _load_module_from_file("newton_sqrt_approx_mod_out", file_path)
    out = capsys.readouterr().out.strip()

    m = re.search(r"Approx sqrt:\s*([-+]?\d+(?:\.\d+)?)\s*$", out)
    assert m is not None, f"expected=parsable_numeric_output actual={out!r}"

    approx = float(m.group(1))
    expected = math.sqrt(getattr(mod, "value", 25.0))
    assert math.isfinite(approx), f"expected=finite actual={approx!r}"
    assert abs(approx - expected) < 1e-5, f"expected={expected} actual={approx}"


def test_converges_within_tolerance_from_module_vars(capsys):
    file_path = Path(__file__).resolve().parent / "10_newtonSqrtApprox.py"
    mod = _load_module_from_file("newton_sqrt_approx_mod_tol", file_path)
    capsys.readouterr()

    value = float(getattr(mod, "value"))
    tol = float(getattr(mod, "tolerance"))
    x = float(getattr(mod, "x"))

    expected = math.sqrt(value)
    err = abs(x - expected)
    assert err <= max(1e-12, tol * 10), f"expected<={max(1e-12, tol * 10)} actual={err}"


def test_newton_fixed_point_residual_small(capsys):
    file_path = Path(__file__).resolve().parent / "10_newtonSqrtApprox.py"
    mod = _load_module_from_file("newton_sqrt_approx_mod_res", file_path)
    capsys.readouterr()

    value = float(getattr(mod, "value"))
    tol = float(getattr(mod, "tolerance"))
    x = float(getattr(mod, "x"))

    residual = abs(x * x - value)
    threshold = max(1e-12, tol * max(1.0, value) * 10)
    assert residual <= threshold, f"expected<={threshold} actual={residual}"