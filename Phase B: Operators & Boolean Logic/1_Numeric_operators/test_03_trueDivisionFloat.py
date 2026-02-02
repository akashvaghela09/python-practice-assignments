import importlib.util
import io
import os
import sys


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_exact_average_output(capfd):
    target = os.path.join(os.path.dirname(__file__), "03_trueDivisionFloat.py")
    load_module_from_path("mod_03_trueDivisionFloat", target)
    out = capfd.readouterr().out
    expected = "Average: 12.5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_average_value_is_float_12_5():
    target = os.path.join(os.path.dirname(__file__), "03_trueDivisionFloat.py")
    old_stdout = sys.stdout
    try:
        sys.stdout = io.StringIO()
        m = load_module_from_path("mod_03_trueDivisionFloat_val", target)
    finally:
        sys.stdout = old_stdout

    expected = 12.5
    actual = getattr(m, "average", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, float), f"expected={float!r} actual={type(actual)!r}"