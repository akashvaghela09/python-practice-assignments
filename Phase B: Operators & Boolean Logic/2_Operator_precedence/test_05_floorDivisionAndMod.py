import importlib.util
import io
import os
import re
import sys


def _load_module_from_path(path, module_name="student_mod_05"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_output(path):
    old_stdout = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        _load_module_from_path(path, module_name="student_mod_05_run")
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_script_prints_exact_expected_output():
    path = os.path.join(os.path.dirname(__file__), "05_floorDivisionAndMod.py")
    out = _run_script_capture_output(path)
    expected = "q=3\nr=2\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_has_no_unfilled_placeholders():
    path = os.path.join(os.path.dirname(__file__), "05_floorDivisionAndMod.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    placeholders = re.findall(r"(?m)^.*\b__\b.*$", content)
    assert placeholders == [], f"expected={[]} actual={placeholders!r}"


def test_q_and_r_values_after_execution():
    path = os.path.join(os.path.dirname(__file__), "05_floorDivisionAndMod.py")
    mod = _load_module_from_path(path, module_name="student_mod_05_values")
    expected_q, expected_r = 3, 2
    actual_q = getattr(mod, "q", None)
    actual_r = getattr(mod, "r", None)
    assert (expected_q, expected_r) == (actual_q, actual_r), f"expected={(expected_q, expected_r)!r} actual={(actual_q, actual_r)!r}"