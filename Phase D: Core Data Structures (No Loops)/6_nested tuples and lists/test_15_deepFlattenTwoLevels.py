import importlib.util
import os
import sys


def _load_module_from_filename(filename):
    test_dir = os.path.dirname(__file__)
    path = os.path.join(test_dir, filename)
    assert os.path.exists(path), f"missing file: {filename}"
    module_name = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_prints_expected_list(capsys):
    _load_module_from_filename("15_deepFlattenTwoLevels.py")
    out = capsys.readouterr().out.strip()
    expected = str([1, 2, 3, 4, 5, 6])
    assert out == expected, f"expected {expected} got {out}"


def test_flat_variable_is_correct():
    mod = _load_module_from_filename("15_deepFlattenTwoLevels.py")
    expected = [1, 2, 3, 4, 5, 6]
    assert hasattr(mod, "flat"), "flat missing"
    assert mod.flat == expected, f"expected {expected} got {mod.flat}"


def test_flat_is_list_of_ints_in_order():
    mod = _load_module_from_filename("15_deepFlattenTwoLevels.py")
    expected = [1, 2, 3, 4, 5, 6]
    actual = mod.flat
    assert isinstance(actual, list), f"expected {type(expected)} got {type(actual)}"
    assert all(isinstance(x, int) for x in actual), f"expected all-int list got {actual}"
    assert actual == expected, f"expected {expected} got {actual}"