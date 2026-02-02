import importlib.util
import os
import sys
import pytest


MODULE_NAME = "10_typeValidationFunction"
FILE_NAME = "10_typeValidationFunction.py"


def _load_module():
    test_dir = os.path.dirname(__file__)
    file_path = os.path.join(test_dir, FILE_NAME)
    if not os.path.exists(file_path):
        file_path = os.path.abspath(FILE_NAME)

    spec = importlib.util.spec_from_file_location(MODULE_NAME, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_printed_output_on_import(capsys):
    _load_module()
    captured = capsys.readouterr()
    expected = "ok:int\nok:float\nerror:expected number\nok:bool\nerror:expected number\n"
    assert captured.out == expected, f"expected={expected!r} actual={captured.out!r}"


@pytest.mark.parametrize(
    "value, expected",
    [
        (5, "ok:int"),
        (2.5, "ok:float"),
        ("3", "error:expected number"),
        (True, "ok:bool"),
        (False, "ok:bool"),
        (None, "error:expected number"),
        ([], "error:expected number"),
        ({}, "error:expected number"),
        (3+0j, "error:expected number"),
    ],
)
def test_classify_number_values(value, expected):
    mod = _load_module()
    actual = mod.classify_number(value)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_int_vs_bool_distinction():
    mod = _load_module()
    expected_int = "ok:int"
    expected_bool = "ok:bool"
    actual_int = mod.classify_number(1)
    actual_bool = mod.classify_number(True)
    assert actual_int == expected_int, f"expected={expected_int!r} actual={actual_int!r}"
    assert actual_bool == expected_bool, f"expected={expected_bool!r} actual={actual_bool!r}"