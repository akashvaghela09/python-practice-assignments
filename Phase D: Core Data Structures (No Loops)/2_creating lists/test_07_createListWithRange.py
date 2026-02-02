import importlib.util
import os
import sys
import ast
import re
import pytest

FILE_NAME = "07_createListWithRange.py"


def _load_module(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("student_mod_07", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["student_mod_07"] = mod
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def _expected_list():
    return list(range(2, 13, 2))


def _extract_printed_list(output):
    s = output.strip()
    if not s:
        return None
    last_line = s.splitlines()[-1].strip()
    try:
        val = ast.literal_eval(last_line)
    except Exception:
        return None
    return val


def _find_assignment_source():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_evens_variable_exists_and_correct(capsys):
    mod, _ = _load_module(capsys)
    assert hasattr(mod, "evens")
    expected = _expected_list()
    actual = mod.evens
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_expected_list(capsys):
    _, out = _load_module(capsys)
    expected = _expected_list()
    printed = _extract_printed_list(out)
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_uses_range_in_source():
    src = _find_assignment_source()
    assert re.search(r"\brange\s*\(", src) is not None


def test_no_hardcoded_full_list_literal():
    src = _find_assignment_source()
    compact = re.sub(r"\s+", "", src)
    assert "[2,4,6,8,10,12]" not in compact