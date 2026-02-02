import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

import pytest


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_last_printed_dict(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    assert lines, "no output"
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception as e:
        raise AssertionError("output not a valid literal") from e
    assert isinstance(val, dict), "output not a dict"
    return val


def test_passed_dict_output(tmp_path):
    path = os.path.join(os.path.dirname(__file__), "06_filterByValue.py")
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = load_module_from_path("m06_filterByValue_out", path)
    out = buf.getvalue()
    printed = parse_last_printed_dict(out)

    expected = {k: v for k, v in getattr(mod, "scores").items() if v >= 8}
    actual = printed
    assert actual == expected, f"expected={expected} actual={actual}"


def test_passed_variable_matches_condition_and_is_new_dict():
    path = os.path.join(os.path.dirname(__file__), "06_filterByValue.py")
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = load_module_from_path("m06_filterByValue_var", path)

    assert hasattr(mod, "scores")
    assert hasattr(mod, "passed")
    assert isinstance(mod.scores, dict)
    assert isinstance(mod.passed, dict)

    expected = {k: v for k, v in mod.scores.items() if v >= 8}
    actual = mod.passed
    assert actual == expected, f"expected={expected} actual={actual}"
    assert mod.passed is not mod.scores, f"expected={'different_objects'} actual={'same_object'}"


def test_does_not_mutate_scores():
    path = os.path.join(os.path.dirname(__file__), "06_filterByValue.py")
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = load_module_from_path("m06_filterByValue_scores", path)

    expected = {"a": 3, "b": 12, "c": 5, "d": 9}
    actual = mod.scores
    assert actual == expected, f"expected={expected} actual={actual}"