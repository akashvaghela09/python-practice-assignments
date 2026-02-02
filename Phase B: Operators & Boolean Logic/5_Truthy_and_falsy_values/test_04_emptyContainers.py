import ast
import io
import os
import runpy
import contextlib
import pytest

MODULE_FILE = "04_emptyContainers.py"


def test_module_file_exists():
    assert os.path.exists(MODULE_FILE)


def test_placeholder_replaced():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    assert "__" not in src


def test_code_compiles():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    compile(src, MODULE_FILE, "exec")


def test_prints_no_items_only():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(MODULE_FILE, run_name="__main__")
    out = buf.getvalue().strip().splitlines()
    assert len(out) == 1
    assert out[0] == "NO ITEMS"


def test_condition_uses_items_name_somewhere_in_if_test():
    src = open(MODULE_FILE, "r", encoding="utf-8").read()
    tree = ast.parse(src, filename=MODULE_FILE)
    if_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.If)]
    assert len(if_nodes) >= 1

    def has_items_name(node):
        return any(isinstance(x, ast.Name) and x.id == "items" for x in ast.walk(node))

    assert any(has_items_name(n.test) for n in if_nodes)