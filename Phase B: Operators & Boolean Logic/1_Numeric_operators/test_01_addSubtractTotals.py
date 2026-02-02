import importlib.util
import os
import sys


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_exact_total_output(capsys):
    file_name = "01_addSubtractTotals.py"
    path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.exists(path):
        path = file_name

    module_name = "mod_01_addSubtractTotals"
    if module_name in sys.modules:
        del sys.modules[module_name]

    _load_module(path, module_name)
    captured = capsys.readouterr()
    expected = "Total: 23\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_total_is_computed_variable_value():
    import importlib

    if "01_addSubtractTotals" in sys.modules:
        del sys.modules["01_addSubtractTotals"]
    m = importlib.import_module("01_addSubtractTotals")

    expected = 23
    actual = getattr(m, "total", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_total_is_numeric_and_not_none():
    import importlib

    if "01_addSubtractTotals" in sys.modules:
        del sys.modules["01_addSubtractTotals"]
    m = importlib.import_module("01_addSubtractTotals")

    actual = getattr(m, "total", None)
    expected_type = int
    assert actual is not None, f"expected={True!r} actual={False!r}"
    assert isinstance(actual, (int, float)), f"expected={(int, float)!r} actual={type(actual)!r}"
    assert isinstance(actual, expected_type), f"expected={expected_type!r} actual={type(actual)!r}"