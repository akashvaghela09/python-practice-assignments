import importlib.util
import os
import sys
import types
import pytest

MODULE_NAME = "13_flattenList"
FILE_NAME = "13_flattenList.py"


def load_module(path):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runs_and_prints_expected_flattened_list(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    try:
        load_module(path)
    except Exception as e:
        pytest.fail(f"{type(e).__name__}: {e}")

    out = capsys.readouterr().out.strip()
    expected = str([1, 2, 3, 4, 5, 6])
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_flat_variable_exists_and_is_correct_when_importable(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    try:
        mod = load_module(path)
    except Exception as e:
        pytest.fail(f"{type(e).__name__}: {e}")

    assert hasattr(mod, "flat"), "expected=attribute 'flat' present actual=missing"
    expected = [1, 2, 3, 4, 5, 6]
    actual = getattr(mod, "flat")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, list), f"expected={list.__name__} actual={type(actual).__name__}"


def test_uses_given_nested_data_if_exposed():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    try:
        mod = load_module(path)
    except Exception as e:
        pytest.fail(f"{type(e).__name__}: {e}")

    if hasattr(mod, "nested"):
        expected_nested = [[1, 2], [3], [4, 5, 6]]
        actual_nested = mod.nested
        assert actual_nested == expected_nested, f"expected={expected_nested!r} actual={actual_nested!r}"