import importlib.util
import os
import sys
import ast
import pytest

FILE_NAME = "02_listAppendAndLength.py"


def _load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    if not os.path.exists(src):
        src = FILE_NAME
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("mod_under_test", str(dst))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(tmp_path, capsys):
    _load_module(tmp_path)
    return capsys.readouterr().out


def test_prints_list_and_length_exact(tmp_path, capsys):
    out = _run_script_capture_stdout(tmp_path, capsys)
    lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 2, f"expected lines=2 actual lines={len(lines)}"
    assert lines[0] == "['milk', 'bread', 'eggs']", f"expected={repr(\"['milk', 'bread', 'eggs']\")} actual={repr(lines[0])}"
    assert lines[1] == "3", f"expected={repr('3')} actual={repr(lines[1])}"


def test_shopping_variable_is_list_and_contents(tmp_path):
    m = _load_module(tmp_path)
    assert isinstance(m.shopping, list), f"expected={repr('list')} actual={repr(type(m.shopping).__name__)}"
    assert m.shopping == ["milk", "bread", "eggs"], f"expected={repr(['milk','bread','eggs'])} actual={repr(m.shopping)}"
    assert len(m.shopping) == 3, f"expected={repr(3)} actual={repr(len(m.shopping))}"


def test_uses_append_calls_three_times(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    if not os.path.exists(src):
        src = FILE_NAME
    code = open(src, "r", encoding="utf-8").read()
    tree = ast.parse(code)

    append_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "append":
            append_calls.append(node)

    assert len(append_calls) == 3, f"expected={repr(3)} actual={repr(len(append_calls))}"


def test_no_reassignment_of_shopping(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    if not os.path.exists(src):
        src = FILE_NAME
    code = open(src, "r", encoding="utf-8").read()
    tree = ast.parse(code)

    assigns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "shopping":
                    assigns.append(node)
        if isinstance(node, ast.AnnAssign):
            t = node.target
            if isinstance(t, ast.Name) and t.id == "shopping":
                assigns.append(node)

    assert len(assigns) == 1, f"expected={repr(1)} actual={repr(len(assigns))}"