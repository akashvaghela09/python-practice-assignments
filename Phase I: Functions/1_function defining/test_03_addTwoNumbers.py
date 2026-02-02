import ast
import importlib.util
import io
import os
import sys
import contextlib

MODULE_FILE = "03_addTwoNumbers.py"


def load_module_from_path(path, name="student_mod"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prints_expected_sum(capsys):
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    load_module_from_path(path, name="mod_print_test")
    captured = capsys.readouterr()
    actual = captured.out.strip()
    expected = "12"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_add_function_exists_and_works_without_import_side_effects(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src_path, "r", encoding="utf-8").read()
    tree = ast.parse(code, filename=MODULE_FILE)

    func_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "add":
            func_node = node
            break
    assert func_node is not None

    mod_ast = ast.Module(body=[func_node], type_ignores=[])
    compiled = compile(mod_ast, filename=MODULE_FILE, mode="exec")
    ns = {}
    exec(compiled, ns, ns)

    add = ns.get("add")
    assert callable(add)

    expected = 12
    actual = add(7, 5)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    expected = -1
    actual = add(2, -3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_total_variable_matches_add_call(capsys):
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    mod = load_module_from_path(path, name="mod_total_test")
    capsys.readouterr()

    assert hasattr(mod, "add")
    assert hasattr(mod, "total")

    expected = mod.add(7, 5)
    actual = mod.total
    assert actual == expected, f"expected={expected!r} actual={actual!r}"