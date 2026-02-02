import ast
import importlib.util
import io
import os
import sys
import pytest

MODULE_FILENAME = "01_createEmptyAndPrint.py"


def _load_module(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    if not os.path.exists(src_path):
        pytest.skip(f"Missing source file: {MODULE_FILENAME}")
    code = open(src_path, "r", encoding="utf-8").read()

    tmp_file = tmp_path / MODULE_FILENAME
    tmp_file.write_text(code, encoding="utf-8")

    mod_name = "student_module_01"
    spec = importlib.util.spec_from_file_location(mod_name, str(tmp_file))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(mod_name, None)
    spec.loader.exec_module(module)
    return module, code


def test_items_defined_as_empty_list_and_printed(tmp_path, capsys):
    module, code = _load_module(tmp_path)

    assert hasattr(module, "items"), f"expected items to exist vs actual missing"
    assert isinstance(module.items, list), f"expected type list vs actual {type(module.items).__name__}"
    assert module.items == [], f"expected [] vs actual {module.items!r}"

    captured = capsys.readouterr()
    out = captured.out
    err = captured.err

    expected_out = "[]\n"
    assert err == "", f"expected '' vs actual {err!r}"
    assert out == expected_out, f"expected {expected_out!r} vs actual {out!r}"


def test_source_assigns_items_and_prints_it(tmp_path):
    _, code = _load_module(tmp_path)

    tree = ast.parse(code)

    assigns_items = False
    prints_items = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "items":
                    assigns_items = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            if node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == "items":
                prints_items = True

    assert assigns_items is True, f"expected True vs actual {assigns_items}"
    assert prints_items is True, f"expected True vs actual {prints_items}"