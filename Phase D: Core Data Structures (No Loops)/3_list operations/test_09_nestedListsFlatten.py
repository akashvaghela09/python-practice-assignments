import importlib.util
import os
import re
import sys
from pathlib import Path


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_printed_flattened_list(capsys):
    file_path = Path(__file__).resolve().parent / "09_nestedListsFlatten.py"
    _load_module("nestedlistsflatten_09_print", file_path)
    captured = capsys.readouterr()
    out = captured.out.strip()
    assert re.fullmatch(r"flat=\[1, 2, 3, 4, 5, 6\]", out), f"expected={r'flat=[1, 2, 3, 4, 5, 6]'} actual={out}"


def test_flat_variable_value(capsys):
    file_path = Path(__file__).resolve().parent / "09_nestedListsFlatten.py"
    mod = _load_module("nestedlistsflatten_09_var", file_path)
    capsys.readouterr()
    expected = [1, 2, 3, 4, 5, 6]
    actual = getattr(mod, "flat", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_matrix_unchanged(capsys):
    file_path = Path(__file__).resolve().parent / "09_nestedListsFlatten.py"
    mod = _load_module("nestedlistsflatten_09_matrix", file_path)
    capsys.readouterr()
    expected = [[1, 2], [3], [4, 5, 6]]
    actual = getattr(mod, "matrix", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_flat_is_new_list_not_alias_of_matrix(capsys):
    file_path = Path(__file__).resolve().parent / "09_nestedListsFlatten.py"
    mod = _load_module("nestedlistsflatten_09_alias", file_path)
    capsys.readouterr()
    matrix = getattr(mod, "matrix", None)
    flat = getattr(mod, "flat", None)
    assert flat is not matrix, f"expected={'different objects'} actual={'same object' if flat is matrix else 'different objects'}"
    if isinstance(matrix, list) and matrix:
        assert flat is not matrix[0], f"expected={'not alias'} actual={'alias' if flat is matrix[0] else 'not alias'}"