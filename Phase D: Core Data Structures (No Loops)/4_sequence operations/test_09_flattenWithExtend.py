import importlib.util
import os
import sys
import ast
import pytest

MODULE_FILENAME = "09_flattenWithExtend.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("student_mod_09_flattenWithExtend", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_source():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def flatten_expected(matrix):
    out = []
    for row in matrix:
        for x in row:
            out.append(x)
    return out


def test_module_imports_without_error(capsys):
    mod = load_module()
    assert hasattr(mod, "matrix")
    assert hasattr(mod, "flat")


def test_flat_is_correct_value(capsys):
    mod = load_module()
    expected = flatten_expected(mod.matrix)
    actual = mod.flat
    assert actual == expected, f"expected={expected} actual={actual}"


def test_flat_is_list_and_new_object(capsys):
    mod = load_module()
    assert isinstance(mod.flat, list)
    assert mod.flat is not mod.matrix


def test_flat_is_one_level_only_not_nested(capsys):
    mod = load_module()
    expected = flatten_expected(mod.matrix)
    actual = mod.flat
    assert all(not isinstance(x, list) for x in actual), f"expected={expected} actual={actual}"


def test_constraints_no_sum_no_itertools_no_list_comprehensions():
    src = get_source()

    tree = ast.parse(src)

    class Finder(ast.NodeVisitor):
        def __init__(self):
            self.has_listcomp = False
            self.uses_sum = False
            self.imports_itertools = False

        def visit_ListComp(self, node):
            self.has_listcomp = True
            self.generic_visit(node)

        def visit_GeneratorExp(self, node):
            self.has_listcomp = True
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "sum":
                self.uses_sum = True
            self.generic_visit(node)

        def visit_Import(self, node):
            for alias in node.names:
                if alias.name == "itertools":
                    self.imports_itertools = True
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.module == "itertools":
                self.imports_itertools = True
            self.generic_visit(node)

    f = Finder()
    f.visit(tree)

    assert not f.uses_sum
    assert not f.imports_itertools
    assert not f.has_listcomp


def test_uses_extend_or_equivalent_row_addition():
    src = get_source()
    tree = ast.parse(src)

    class ExtendChecker(ast.NodeVisitor):
        def __init__(self):
            self.found_extend = False
            self.found_iadd = False
            self.found_add_assign = False

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr == "extend":
                self.found_extend = True
            self.generic_visit(node)

        def visit_AugAssign(self, node):
            if isinstance(node.op, ast.Add):
                self.found_iadd = True
            self.generic_visit(node)

        def visit_Assign(self, node):
            self.generic_visit(node)

    c = ExtendChecker()
    c.visit(tree)

    assert (c.found_extend or c.found_iadd), f"expected={True} actual={(c.found_extend or c.found_iadd)}"