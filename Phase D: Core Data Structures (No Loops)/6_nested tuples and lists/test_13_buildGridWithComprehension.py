import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

import pytest


ASSIGNMENT_FILE = "13_buildGridWithComprehension.py"


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_13", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_printed_output_exact():
    mod, out = _run_script_capture_stdout(ASSIGNMENT_FILE)
    expected = "[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_grid_structure_and_independence():
    mod, _ = _run_script_capture_stdout(ASSIGNMENT_FILE)
    grid = getattr(mod, "grid", None)

    assert isinstance(grid, list), f"expected={list} actual={type(grid)}"
    assert len(grid) == 3, f"expected={3} actual={len(grid)}"

    for r in grid:
        assert isinstance(r, list), f"expected={list} actual={type(r)}"
        assert len(r) == 4, f"expected={4} actual={len(r)}"
        assert all(x == 0 for x in r), f"expected={True} actual={all(x == 0 for x in r)}"

    assert all(grid[i] is not grid[j] for i in range(len(grid)) for j in range(i + 1, len(grid))), (
        f"expected={True} actual={any(grid[i] is grid[j] for i in range(len(grid)) for j in range(i + 1, len(grid)))}"
    )

    # mutation independence check
    before = [row[:] for row in grid]
    grid[0][0] = 1
    unchanged = grid[1][0] == before[1][0] and grid[2][0] == before[2][0]
    assert unchanged, f"expected={True} actual={unchanged}"


def test_uses_list_comprehension_for_grid_not_list_multiplication():
    with open(ASSIGNMENT_FILE, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    assigns = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "grid":
                    assigns.append(node)

    assert assigns, f"expected={True} actual={False}"

    grid_assign = assigns[-1].value

    is_listcomp = isinstance(grid_assign, ast.ListComp)
    assert is_listcomp, f"expected={True} actual={is_listcomp}"

    class _MulDetector(ast.NodeVisitor):
        def __init__(self):
            self.has_mult = False

        def visit_BinOp(self, node):
            if isinstance(node.op, ast.Mult):
                self.has_mult = True
            self.generic_visit(node)

    md = _MulDetector()
    md.visit(grid_assign)
    assert (not md.has_mult), f"expected={False} actual={md.has_mult}"


def test_rows_cols_constants_present_and_used():
    mod, _ = _run_script_capture_stdout(ASSIGNMENT_FILE)
    assert getattr(mod, "rows", None) == 3, f"expected={3} actual={getattr(mod, 'rows', None)!r}"
    assert getattr(mod, "cols", None) == 4, f"expected={4} actual={getattr(mod, 'cols', None)!r}"

    with open(ASSIGNMENT_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    grid_assign = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "grid" for t in node.targets):
            grid_assign = node.value

    assert isinstance(grid_assign, ast.ListComp), f"expected={ast.ListComp} actual={type(grid_assign)}"

    names = set()

    class _NameCollector(ast.NodeVisitor):
        def visit_Name(self, node):
            names.add(node.id)

    _NameCollector().visit(grid_assign)
    uses_rows_cols = ("rows" in names) and ("cols" in names)
    assert uses_rows_cols, f"expected={True} actual={uses_rows_cols}"