import importlib
import io
import contextlib
import pathlib
import ast
import pytest

MODULE_NAME = "02_basicTernary_evenOddLabel"


def _load_source():
    path = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    return path.read_text(encoding="utf-8")


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def test_output_is_exactly_odd(monkeypatch):
    monkeypatch.delitem(importlib.sys.modules, MODULE_NAME, raising=False)
    out = _run_module_capture_stdout()
    expected = "odd\n"
    actual = out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_conditional_expression_for_label():
    src = _load_source()
    tree = ast.parse(src)
    assigns = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "label" for t in node.targets)
    ]
    assert assigns, "expected='label assignment exists' actual='missing'"
    value = assigns[0].value
    expected = "IfExp"
    actual = type(value).__name__ if value is not None else None
    assert isinstance(value, ast.IfExp), f"expected={expected!r} actual={actual!r}"


def test_label_contains_even_and_odd_literals():
    src = _load_source()
    tree = ast.parse(src)
    assigns = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "label" for t in node.targets)
    ]
    assert assigns, "expected='label assignment exists' actual='missing'"

    value = assigns[0].value
    literals = set()
    for node in ast.walk(value):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.add(node.value)

    expected = {"even", "odd"}
    actual = literals
    assert expected.issubset(actual), f"expected={sorted(expected)!r} actual={sorted(actual)!r}"


def test_prints_label_variable_not_string_literal():
    src = _load_source()
    tree = ast.parse(src)
    print_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
    ]
    assert print_calls, "expected='print call exists' actual='missing'"

    call = print_calls[-1]
    arg = call.args[0] if call.args else None
    expected = "Name(label)"
    actual = (
        f"{type(arg).__name__}({getattr(arg, 'id', None)})" if arg is not None else None
    )
    assert isinstance(arg, ast.Name) and arg.id == "label", f"expected={expected!r} actual={actual!r}"