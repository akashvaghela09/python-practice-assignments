import importlib
import contextlib
import io
import ast
import re


def _run_module_capture_stdout(module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_printed_unique_list_exact():
    out = _run_module_capture_stdout("08_unique_preserve_order")
    expected = "unique: [3, 1, 2, 4]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_unique_variable_value():
    mod = importlib.import_module("08_unique_preserve_order")
    expected = [3, 1, 2, 4]
    actual = getattr(mod, "unique", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_not_in_in_condition():
    mod = importlib.import_module("08_unique_preserve_order")
    path = getattr(mod, "__file__", None)
    assert path is not None
    src = open(path, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test
            if isinstance(test, ast.Compare) and any(isinstance(op, ast.NotIn) for op in test.ops):
                found = True
                break

    expected = True
    actual = found
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_does_not_use_set_for_uniqueness():
    mod = importlib.import_module("08_unique_preserve_order")
    path = getattr(mod, "__file__", None)
    src = open(path, "r", encoding="utf-8").read()

    uses_set_ctor = bool(re.search(r"\bset\s*\(", src))
    uses_set_literal = "{" in src and "}" in src and "set(" not in src

    expected = False
    actual = uses_set_ctor or uses_set_literal
    assert actual == expected, f"expected={expected!r} actual={actual!r}"