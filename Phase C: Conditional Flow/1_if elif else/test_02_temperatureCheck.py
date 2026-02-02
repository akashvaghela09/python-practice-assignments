import importlib.util
import io
import os
import sys

import pytest


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location(module_filename[:-3], path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_prints_single_valid_label():
    out = _run_module_capture_stdout("02_temperatureCheck.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1
    assert lines[0] in {"Cold", "Warm", "Hot"}


def test_temp_22_prints_warm(capsys):
    out = _run_module_capture_stdout("02_temperatureCheck.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    expected = "Warm"
    actual = lines[0] if lines else ""
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_has_no_extra_whitespace_or_text():
    out = _run_module_capture_stdout("02_temperatureCheck.py")
    stripped = out.strip()
    expected_set = {"Cold", "Warm", "Hot"}
    actual = stripped
    assert actual in expected_set, f"expected={sorted(expected_set)!r} actual={actual!r}"
    assert out in {"Cold\n", "Warm\n", "Hot\n", "Cold", "Warm", "Hot"}