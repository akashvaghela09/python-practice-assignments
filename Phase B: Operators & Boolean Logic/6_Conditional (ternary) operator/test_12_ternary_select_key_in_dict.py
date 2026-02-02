import importlib
import io
import os
import re
import sys
import types
import pytest

MODULE_NAME = "12_ternary_select_key_in_dict"


def _run_module_capture_stdout():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.import_module(MODULE_NAME)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_expected_token_value():
    out = _run_module_capture_stdout()
    expected = "token=BK-999\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_output_has_single_line_and_no_extra_whitespace():
    out = _run_module_capture_stdout()
    expected_lines = ["token=BK-999"]
    actual_lines = out.splitlines()
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_key_is_selected_via_ternary_expression_in_source():
    mod = importlib.import_module(MODULE_NAME)
    path = getattr(mod, "__file__", None)
    assert path and os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    src_no_comments = "\n".join(line.split("#", 1)[0] for line in src.splitlines())

    key_line = None
    for line in src_no_comments.splitlines():
        if re.match(r"^\s*key\s*=", line):
            key_line = line.strip()
            break

    assert key_line is not None, f"expected={'key assignment line present'!r} actual={None!r}"
    has_if_else = bool(re.search(r"\bif\b.*\belse\b", key_line))
    assert has_if_else is True, f"expected={True!r} actual={has_if_else!r}"


def test_ternary_references_use_primary_and_expected_keys_in_source():
    mod = importlib.import_module(MODULE_NAME)
    path = getattr(mod, "__file__", None)
    assert path and os.path.exists(path)

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    src_no_comments = "\n".join(line.split("#", 1)[0] for line in src.splitlines())

    key_line = None
    for line in src_no_comments.splitlines():
        if re.match(r"^\s*key\s*=", line):
            key_line = line.strip()
            break

    assert key_line is not None, f"expected={'key assignment line present'!r} actual={None!r}"
    uses_var = "use_primary" in key_line
    has_primary = '"primary"' in key_line or "'primary'" in key_line
    has_backup = '"backup"' in key_line or "'backup'" in key_line

    expected = (True, True, True)
    actual = (uses_var, has_primary, has_backup)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"