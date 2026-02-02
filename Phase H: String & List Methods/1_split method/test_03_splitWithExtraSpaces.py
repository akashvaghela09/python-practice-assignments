import ast
import importlib
import io
import os
import sys
import contextlib
import pytest

MODULE_NAME = "03_splitWithExtraSpaces"


def run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.invalidate_caches()
        if MODULE_NAME in sys.modules:
            del sys.modules[MODULE_NAME]
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def test_prints_expected_list():
    out = run_module_capture_stdout().strip()
    try:
        val = ast.literal_eval(out)
    except Exception as e:
        pytest.fail(f"expected={['Too','many','spaces']} actual={out}")
    expected = ["Too", "many", "spaces"]
    assert val == expected, f"expected={expected} actual={val}"


def test_words_variable_created_and_correct():
    importlib.invalidate_caches()
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    with contextlib.redirect_stdout(io.StringIO()):
        mod = importlib.import_module(MODULE_NAME)
    expected = ["Too", "many", "spaces"]
    actual = getattr(mod, "words", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_source_has_placeholder_to_fill():
    here = os.path.dirname(__file__)
    path = os.path.join(here, f"{MODULE_NAME}.py")
    if not os.path.exists(path):
        pytest.skip(f"expected={path} actual=missing")
    src = open(path, "r", encoding="utf-8").read()
    assert "___" in src, f"expected=placeholder actual=absent"