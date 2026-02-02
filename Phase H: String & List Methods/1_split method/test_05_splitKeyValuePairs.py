import importlib.util
import io
import os
import contextlib
import pytest


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_split_key_value_pairs_prints_expected_output():
    path = os.path.join(os.path.dirname(__file__), "05_splitKeyValuePairs.py")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        load_module(path, "m05_splitKeyValuePairs")
    out = buf.getvalue().strip()
    expected = "mode -> debug"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_source_contains_no_placeholder():
    path = os.path.join(os.path.dirname(__file__), "05_splitKeyValuePairs.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "___" not in src, f"expected={'no placeholder'} actual={'placeholder found'}"