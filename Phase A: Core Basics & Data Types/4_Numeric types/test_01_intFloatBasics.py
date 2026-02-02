import importlib
import io
import sys
import pytest

MODULE_NAME = "01_intFloatBasics"

def import_fresh(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)

def test_outputs_exact_types_in_order(capsys):
    import_fresh(MODULE_NAME)
    captured = capsys.readouterr()
    expected = "<class 'int'>\n<class 'float'>\n"
    assert captured.out == expected, f"expected={expected!r} actual={captured.out!r}"

def test_variables_exist_and_have_correct_types():
    m = import_fresh(MODULE_NAME)
    assert hasattr(m, "age"), "expected=True actual=False"
    assert hasattr(m, "pi"), "expected=True actual=False"
    assert isinstance(m.age, int), f"expected={int} actual={type(m.age)}"
    assert isinstance(m.pi, float), f"expected={float} actual={type(m.pi)}"