import importlib.util
import os
import sys


def load_module():
    filename = "07_iterateAndBuildResultTuple.py"
    module_name = "mod_07_iterateAndBuildResultTuple"
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(os.getcwd(), filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_nums_is_unchanged():
    m = load_module()
    assert hasattr(m, "nums")
    assert m.nums == (1, 2, 3, 4)


def test_squared_is_tuple_and_correct():
    m = load_module()
    assert hasattr(m, "squared")
    assert isinstance(m.squared, tuple)
    expected = tuple(x * x for x in m.nums)
    assert m.squared == expected


def test_prints_squared(capsys):
    m = load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) >= 1
    expected_line = str(tuple(x * x for x in m.nums))
    assert out[-1] == expected_line


def test_squared_is_new_object_not_same_as_nums():
    m = load_module()
    assert m.squared is not m.nums