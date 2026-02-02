import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILE = "03_basicTernary_absValue.py"


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_module_capture_stdout(path):
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        spec = importlib.util.spec_from_file_location("student_module_run", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_program_prints_exact_expected_output():
    out = run_module_capture_stdout(MODULE_FILE)
    expected = "abs=12\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_abs_x_value_is_correct_when_module_imports():
    module = load_module_from_path(MODULE_FILE, "student_module_import")
    expected = 12
    actual = getattr(module, "abs_x", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_abs_x_uses_conditional_expression_not_builtin_abs_or_if_statement():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()

    src_no_strings = []
    in_str = None
    esc = False
    for ch in src:
        if in_str:
            if esc:
                esc = False
                src_no_strings.append(" ")
                continue
            if ch == "\\":
                esc = True
                src_no_strings.append(" ")
                continue
            if ch == in_str:
                in_str = None
            src_no_strings.append(" ")
        else:
            if ch in ("'", '"'):
                in_str = ch
                src_no_strings.append(" ")
            else:
                src_no_strings.append(ch)
    src_sanitized = "".join(src_no_strings)

    assert "abs(" not in src_sanitized, f"expected={'no abs(...)'} actual={'abs(...) present'}"
    assert "if " not in src_sanitized, f"expected={'no if statement'} actual={'if statement present'}"
    assert " if " in src_sanitized and " else " in src_sanitized, f"expected={'ternary present'} actual={'ternary missing'}"