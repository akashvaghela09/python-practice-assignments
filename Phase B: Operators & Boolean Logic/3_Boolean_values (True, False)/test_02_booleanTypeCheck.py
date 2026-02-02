import importlib.util
import os
import sys
import types
import ast
import pytest

MODULE_FILENAME = "02_booleanTypeCheck.py"


def _load_module_from_file(tmp_path, filename=MODULE_FILENAME):
    src = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(src):
        src = os.path.join(os.getcwd(), filename)
    if not os.path.exists(src):
        raise FileNotFoundError(filename)

    dst = tmp_path / filename
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    mod_name = os.path.splitext(filename)[0]
    spec = importlib.util.spec_from_file_location(mod_name, str(dst))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(mod_name, None)
    spec.loader.exec_module(module)
    return module


def test_prints_bool_type_exactly(capfd, tmp_path):
    _load_module_from_file(tmp_path)
    out, err = capfd.readouterr()
    expected = str(type(False))
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_is_complete_exists_and_is_bool(tmp_path):
    module = _load_module_from_file(tmp_path)
    assert hasattr(module, "is_complete")
    assert isinstance(module.is_complete, bool), f"expected={bool!r} actual={type(module.is_complete)!r}"


def test_has_print_call_expression(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    if not os.path.exists(src):
        src = os.path.join(os.getcwd(), MODULE_FILENAME)
    code = open(src, "r", encoding="utf-8").read()
    tree = ast.parse(code)

    prints = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            prints.append(node)

    assert len(prints) >= 1, f"expected={'>=1'!r} actual={len(prints)!r}"