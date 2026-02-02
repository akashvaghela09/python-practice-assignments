import importlib.util
import os
import sys
import ast
import re

FILE_NAME = "10_nestedListsMatrixRowSums.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("student_mod_10", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_row_sums(matrix):
    res = []
    for row in matrix:
        total = 0
        for v in row:
            total += v
        res.append(total)
    return res


def test_row_sums_value():
    mod = _load_module()
    assert hasattr(mod, "matrix")
    assert hasattr(mod, "row_sums")
    exp = _expected_row_sums(mod.matrix)
    act = mod.row_sums
    assert act == exp, f"expected={exp} actual={act}"


def test_row_sums_structure_and_lengths():
    mod = _load_module()
    assert isinstance(mod.matrix, list)
    assert isinstance(mod.row_sums, list)
    exp = _expected_row_sums(mod.matrix)
    assert len(mod.row_sums) == len(exp), f"expected={len(exp)} actual={len(mod.row_sums)}"
    for i, (a, e) in enumerate(zip(mod.row_sums, exp)):
        assert a == e, f"expected={e} actual={a}"


def test_no_builtin_sum_used_in_source():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            name = None
            if isinstance(fn, ast.Name):
                name = fn.id
            elif isinstance(fn, ast.Attribute):
                name = fn.attr
            if name:
                calls.append(name)

    used_sum = any(name == "sum" for name in calls)
    assert used_sum is False, f"expected={False} actual={used_sum}"


def test_prints_row_sums(capsys):
    mod = _load_module()
    captured = capsys.readouterr()
    out = captured.out.strip()
    exp = str(_expected_row_sums(mod.matrix))
    assert out.endswith(exp), f"expected={exp} actual={out}"