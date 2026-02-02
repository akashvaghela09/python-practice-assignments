import importlib.util
import os
import sys
from io import StringIO

import pytest

MODULE_FILE = "19_pathWalkNestedList.py"


def load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    dst = tmp_path / MODULE_FILE
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("mod19", str(dst))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script_capture_stdout(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    dst = tmp_path / MODULE_FILE
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        spec = importlib.util.spec_from_file_location("run19", str(dst))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return out


def test_prints_expected_value_exactly(tmp_path):
    out = run_script_capture_stdout(tmp_path)
    actual = out
    expected = "99\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_value_matches_walked_path(tmp_path):
    mod = load_module(tmp_path)

    current = mod.data
    for idx in mod.path:
        current = current[idx]

    actual = getattr(mod, "value", object())
    expected = current
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_hardcoded_indexing_present(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src, "r", encoding="utf-8").read()

    forbidden = "data[1][1][1][1]"
    actual = forbidden in code
    expected = False
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_value_is_not_none(tmp_path):
    mod = load_module(tmp_path)
    actual = mod.value is None
    expected = False
    assert actual == expected, f"expected={expected!r} actual={actual!r}"