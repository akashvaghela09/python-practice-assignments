import importlib.util
import os
import sys
import pytest

MODULE_NAME = "09_tupleReturnFromFunction"
FILE_NAME = "09_tupleReturnFromFunction.py"


def _load_module():
    here = os.path.dirname(__file__)
    path = os.path.join(here, FILE_NAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = mod
    spec.loader.exec_module(mod)
    return mod


def test_min_max_returns_tuple_of_two_ints():
    mod = _load_module()
    res = mod.min_max((5, 2, 9, 3))
    assert isinstance(res, tuple), f"expected={tuple} actual={type(res)}"
    assert len(res) == 2, f"expected={2} actual={len(res)}"
    assert all(isinstance(x, int) for x in res), f"expected={'ints'} actual={tuple(type(x) for x in res)}"


def test_min_max_correct_for_sample():
    mod = _load_module()
    values = (5, 2, 9, 3)
    expected = (min(values), max(values))
    actual = mod.min_max(values)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_min_max_correct_for_negatives_and_duplicates():
    mod = _load_module()
    values = (0, -4, -4, 7, 2, 7, 3)
    expected = (min(values), max(values))
    actual = mod.min_max(values)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_min_max_single_element():
    mod = _load_module()
    values = (42,)
    expected = (min(values), max(values))
    actual = mod.min_max(values)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_module_prints_returned_tuple_on_import(capsys):
    _load_module()
    out = capsys.readouterr().out.strip()
    expected = str((2, 9))
    assert out.endswith(expected), f"expected={expected} actual={out}"