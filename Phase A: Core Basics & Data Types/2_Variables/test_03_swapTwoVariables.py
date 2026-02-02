import importlib.util
import io
import os
import re
import contextlib

import pytest


def load_module(path):
    spec = importlib.util.spec_from_file_location("swap_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script_capture(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = load_module(path)
    out = buf.getvalue()
    return mod, out


def test_output_format_and_values():
    path = os.path.join(os.path.dirname(__file__), "03_swapTwoVariables.py")
    mod, out = run_script_capture(path)

    lines = [ln.rstrip("\n") for ln in out.splitlines()]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"

    m1 = re.fullmatch(r"a=(.+)", lines[0])
    m2 = re.fullmatch(r"b=(.+)", lines[1])
    assert m1 is not None, f"expected={'a=<value>'!r} actual={lines[0]!r}"
    assert m2 is not None, f"expected={'b=<value>'!r} actual={lines[1]!r}"

    aval = m1.group(1)
    bval = m2.group(1)

    assert aval.strip() != "", f"expected={'non-empty'!r} actual={aval!r}"
    assert bval.strip() != "", f"expected={'non-empty'!r} actual={bval!r}"

    expected_a = str(getattr(mod, "b", None))
    expected_b = str(getattr(mod, "a", None))
    assert aval == expected_a, f"expected={expected_a!r} actual={aval!r}"
    assert bval == expected_b, f"expected={expected_b!r} actual={bval!r}"


def test_variables_swapped_not_constant_identity():
    path = os.path.join(os.path.dirname(__file__), "03_swapTwoVariables.py")
    mod, out = run_script_capture(path)

    assert hasattr(mod, "a") and hasattr(mod, "b"), f"expected={True!r} actual={False!r}"

    # The printed values must correspond to module variables after execution
    lines = out.splitlines()
    aval = lines[0].split("=", 1)[1]
    bval = lines[1].split("=", 1)[1]

    assert aval == str(mod.a), f"expected={str(mod.a)!r} actual={aval!r}"
    assert bval == str(mod.b), f"expected={str(mod.b)!r} actual={bval!r}"