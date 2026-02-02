import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

import pytest


MODULE_FILENAME = "08_listComprehensionSquares.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("mod08_listComprehensionSquares", path)
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module, path


def parse_module_ast(path):
    with open(path, "r", encoding="utf-8") as f:
        return ast.parse(f.read(), filename=path)


def test_module_imports_without_syntax_error():
    module, _ = load_module()
    assert hasattr(module, "__dict__")


def test_squares_value_and_type():
    module, _ = load_module()
    assert hasattr(module, "squares")
    squares = module.squares
    expected = [i * i for i in range(1, 8)]
    assert isinstance(squares, list)
    assert squares == expected


def test_prints_squares_exactly():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("mod08_listComprehensionSquares_print", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    out = buf.getvalue()
    expected = f"{[i * i for i in range(1, 8)]}\n"
    assert out == expected


def test_uses_list_comprehension_for_squares_assignment():
    _, path = load_module()
    tree = parse_module_ast(path)

    squares_assign = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "squares":
                    squares_assign = node
                    break
        if squares_assign is not None:
            break

    assert squares_assign is not None
    assert isinstance(squares_assign.value, ast.ListComp)

    comp = squares_assign.value
    assert len(comp.generators) == 1
    gen = comp.generators[0]
    assert isinstance(gen.target, ast.Name)
    assert isinstance(gen.iter, ast.Call)
    assert isinstance(gen.iter.func, ast.Name)
    assert gen.iter.func.id == "range"

    args = gen.iter.args
    assert len(args) == 2
    assert isinstance(args[0], ast.Constant) and args[0].value == 1
    assert isinstance(args[1], ast.Constant) and args[1].value == 8

    elt = comp.elt
    assert isinstance(elt, ast.BinOp)
    assert isinstance(elt.op, ast.Mult)
    assert isinstance(elt.left, ast.Name)
    assert isinstance(elt.right, ast.Name)
    assert elt.left.id == gen.target.id
    assert elt.right.id == gen.target.id


def test_print_statement_prints_squares_variable():
    _, path = load_module()
    tree = parse_module_ast(path)

    print_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            print_calls.append(node)

    assert len(print_calls) >= 1

    found = False
    for call in print_calls:
        if len(call.args) == 1 and isinstance(call.args[0], ast.Name) and call.args[0].id == "squares":
            found = True
            break

    assert found