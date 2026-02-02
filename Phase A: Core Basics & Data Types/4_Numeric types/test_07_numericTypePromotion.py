import importlib
import sys
import types


def test_numeric_type_promotion_output(capsys):
    module_name = "07_numericTypePromotion"
    if module_name in sys.modules:
        del sys.modules[module_name]

    importlib.import_module(module_name)
    out = capsys.readouterr().out.splitlines()

    expected_lines = [str(float), str(complex)]
    assert out == expected_lines, f"expected={expected_lines!r} actual={out!r}"


def test_numeric_type_promotion_no_extra_output(capsys):
    module_name = "07_numericTypePromotion"
    if module_name in sys.modules:
        del sys.modules[module_name]

    importlib.import_module(module_name)
    out = capsys.readouterr().out

    expected = f"{str(float)}\n{str(complex)}\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_numeric_type_promotion_variables_exist_and_types():
    module_name = "07_numericTypePromotion"
    if module_name in sys.modules:
        del sys.modules[module_name]

    mod = importlib.import_module(module_name)

    assert hasattr(mod, "result1")
    assert hasattr(mod, "result2")

    expected_types = (float, complex)
    actual_types = (type(mod.result1), type(mod.result2))
    assert actual_types == expected_types, f"expected={expected_types!r} actual={actual_types!r}"