import importlib.util
import io
import os
import contextlib
import re
import pytest

MODULE_FILE = "04_floatRoundingAndFormatting.py"


def _run_module_capture_stdout():
    spec = importlib.util.spec_from_file_location("student_mod_04", MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_module_executes_without_error():
    _run_module_capture_stdout()


def test_prints_two_lines_expected_content_and_format():
    _, out = _run_module_capture_stdout()
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    for i, ln in enumerate(lines):
        assert re.fullmatch(r"-?\d+\.\d{2}", ln) is not None, f"expected={'two-decimal numeric string'!r} actual={ln!r}"
    assert lines[0] == lines[1], f"expected={lines[0]!r} actual={lines[1]!r}"


def test_rounded_is_numeric_and_matches_two_decimal_value():
    mod, out = _run_module_capture_stdout()
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert hasattr(mod, "rounded"), f"expected={'attribute rounded'!r} actual={'missing'!r}"
    assert isinstance(mod.rounded, (int, float)), f"expected={'int|float'!r} actual={type(mod.rounded).__name__!r}"
    assert len(lines) >= 1
    expected_from_output = float(lines[0])
    assert mod.rounded == expected_from_output, f"expected={expected_from_output!r} actual={mod.rounded!r}"


def test_formatted_is_string_and_matches_output_line():
    mod, out = _run_module_capture_stdout()
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert hasattr(mod, "formatted"), f"expected={'attribute formatted'!r} actual={'missing'!r}"
    assert isinstance(mod.formatted, str), f"expected={'str'!r} actual={type(mod.formatted).__name__!r}"
    assert len(lines) >= 2
    assert mod.formatted == lines[1], f"expected={lines[1]!r} actual={mod.formatted!r}"


def test_rounded_equals_round_x_two_decimals():
    mod, _ = _run_module_capture_stdout()
    assert hasattr(mod, "x"), f"expected={'attribute x'!r} actual={'missing'!r}"
    expected = round(mod.x, 2)
    assert mod.rounded == expected, f"expected={expected!r} actual={mod.rounded!r}"


def test_formatted_equals_fstring_two_decimals_of_x():
    mod, _ = _run_module_capture_stdout()
    expected = f"{mod.x:.2f}"
    assert mod.formatted == expected, f"expected={expected!r} actual={mod.formatted!r}"