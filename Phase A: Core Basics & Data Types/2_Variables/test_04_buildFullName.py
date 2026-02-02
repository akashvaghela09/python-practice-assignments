import importlib.util
import io
import os
import sys
import re
import pytest

MODULE_FILENAME = "04_buildFullName.py"


def load_module(path):
    spec = importlib.util.spec_from_file_location("student_module_04_buildFullName", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture(path):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        load_module(path)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_file_exists():
    assert os.path.exists(MODULE_FILENAME)


def test_prints_exact_one_line_and_matches_expected_output():
    out = run_script_capture(MODULE_FILENAME)
    lines = out.splitlines()
    assert len(lines) == 1, f"expected={1} actual={len(lines)}"
    expected_line = "Full name: Ada Lovelace"
    assert lines[0] == expected_line, f"expected={expected_line!r} actual={lines[0]!r}"


def test_full_variable_exists_and_is_correct_string():
    module = load_module(MODULE_FILENAME)
    assert hasattr(module, "full"), f"expected={'full variable present'} actual={'missing'}"
    expected_full = "Ada Lovelace"
    actual_full = getattr(module, "full")
    assert actual_full == expected_full, f"expected={expected_full!r} actual={actual_full!r}"


def test_full_built_from_first_and_last():
    module = load_module(MODULE_FILENAME)
    assert hasattr(module, "first"), f"expected={'first variable present'} actual={'missing'}"
    assert hasattr(module, "last"), f"expected={'last variable present'} actual={'missing'}"
    assert hasattr(module, "full"), f"expected={'full variable present'} actual={'missing'}"
    expected_full = f"{module.first} {module.last}"
    actual_full = module.full
    assert actual_full == expected_full, f"expected={expected_full!r} actual={actual_full!r}"


def test_no_extra_whitespace_in_full():
    module = load_module(MODULE_FILENAME)
    assert hasattr(module, "full"), f"expected={'full variable present'} actual={'missing'}"
    actual_full = module.full
    expected_full = re.sub(r"\s+", " ", actual_full).strip()
    assert actual_full == expected_full, f"expected={expected_full!r} actual={actual_full!r}"