import importlib.util
import ast
import contextlib
import io
import os
import sys


def _load_module_from_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_output(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(path)
    return buf.getvalue()


def test_printed_output_matches_expected_list():
    path = os.path.join(os.path.dirname(__file__), "03_appendExtendInsert.py")
    out = _run_script_capture_output(path).strip()
    expected = '["start", "a", "b", "c", "end"]'
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_items_variable_final_value():
    path = os.path.join(os.path.dirname(__file__), "03_appendExtendInsert.py")
    mod = _load_module_from_path(path)
    expected = ["start", "a", "b", "c", "end"]
    actual = getattr(mod, "items", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_insert_append_extend_calls():
    path = os.path.join(os.path.dirname(__file__), "03_appendExtendInsert.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    methods = {"insert": 0, "append": 0, "extend": 0}

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in methods:
                methods[node.func.attr] += 1

    expected = {"insert": 1, "append": 1, "extend": 1}
    assert methods == expected, f"expected={expected!r} actual={methods!r}"


def test_insert_is_at_beginning_and_extend_uses_singleton_list_c():
    path = os.path.join(os.path.dirname(__file__), "03_appendExtendInsert.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    insert_calls = []
    extend_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "insert":
                insert_calls.append(node)
            elif node.func.attr == "extend":
                extend_calls.append(node)

    assert len(insert_calls) == 1, f"expected={1!r} actual={len(insert_calls)!r}"
    assert len(extend_calls) == 1, f"expected={1!r} actual={len(extend_calls)!r}"

    ins = insert_calls[0]
    ok_insert = (
        len(ins.args) >= 2
        and isinstance(ins.args[0], ast.Constant)
        and ins.args[0].value == 0
        and isinstance(ins.args[1], ast.Constant)
        and ins.args[1].value == "start"
    )
    assert ok_insert is True, f"expected={True!r} actual={ok_insert!r}"

    ext = extend_calls[0]
    ok_extend = (
        len(ext.args) >= 1
        and isinstance(ext.args[0], ast.List)
        and len(ext.args[0].elts) == 1
        and isinstance(ext.args[0].elts[0], ast.Constant)
        and ext.args[0].elts[0].value == "c"
    )
    assert ok_extend is True, f"expected={True!r} actual={ok_extend!r}"