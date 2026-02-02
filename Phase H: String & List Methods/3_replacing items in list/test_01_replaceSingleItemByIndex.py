import importlib.util
import ast
import io
import os
import sys
from contextlib import redirect_stdout

FILE_NAME = "01_replaceSingleItemByIndex.py"


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_module_01", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def _get_ast(path):
    with open(path, "r", encoding="utf-8") as f:
        return ast.parse(f.read(), filename=path)


def test_stdout_matches_expected_list():
    path = os.path.join(os.getcwd(), FILE_NAME)
    _, out = _run_script_capture_stdout(path)
    expected = "['red', 'blue', 'green']\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_colors_variable_is_correct_after_execution():
    path = os.path.join(os.getcwd(), FILE_NAME)
    module, _ = _run_script_capture_stdout(path)
    expected = ["red", "blue", "green"]
    actual = getattr(module, "colors", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_index_assignment_not_remove_or_insert():
    path = os.path.join(os.getcwd(), FILE_NAME)
    tree = _get_ast(path)

    forbidden_methods = {"remove", "insert", "pop", "append", "extend", "clear", "del", "replace"}
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.attr, str)
    ]
    used_forbidden = [c.func.attr for c in calls if c.func.attr in forbidden_methods]

    expected = []
    actual = used_forbidden
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_contains_subscript_assignment_to_colors():
    path = os.path.join(os.getcwd(), FILE_NAME)
    tree = _get_ast(path)

    assigns = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Subscript) for t in node.targets)
    ]

    def is_colors_subscript(sub):
        base = sub.value
        return isinstance(base, ast.Name) and base.id == "colors"

    found = False
    for a in assigns:
        for t in a.targets:
            if isinstance(t, ast.Subscript) and is_colors_subscript(t):
                found = True

    expected = True
    actual = found
    assert actual == expected, f"expected={expected!r} actual={actual!r}"