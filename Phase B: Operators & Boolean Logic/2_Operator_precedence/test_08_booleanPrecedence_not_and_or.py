import importlib
import io
import contextlib
import ast
import pathlib
import pytest

MODULE_NAME = "08_booleanPrecedence_not_and_or"


def _run_module_capture_stdout():
    mod = importlib.import_module(MODULE_NAME)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return buf.getvalue()


def _parse_assignments(source):
    tree = ast.parse(source)
    assigns = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {"A", "B", "C", "result"}:
                assigns[name] = node.value
    return assigns, tree


def _find_print_arg(tree):
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Name) and call.func.id == "print" and len(call.args) == 1:
                return call.args[0]
    return None


def test_prints_exact_true_line():
    out = _run_module_capture_stdout()
    expected = "True\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_A_B_C_are_booleans_and_not_placeholders():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    for name in ("A", "B", "C"):
        assert hasattr(mod, name), f"expected={name!r} actual={'missing'!r}"
        val = getattr(mod, name)
        assert isinstance(val, bool), f"expected={'bool'!r} actual={type(val).__name__!r}"
    assert hasattr(mod, "result"), f"expected={'result'!r} actual={'missing'!r}"
    assert isinstance(mod.result, bool), f"expected={'bool'!r} actual={type(mod.result).__name__!r}"


def test_result_expression_has_no_parentheses_and_correct_operator_structure():
    path = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    source = path.read_text(encoding="utf-8")
    assigns, tree = _parse_assignments(source)

    assert "result" in assigns, f"expected={'result assigned'!r} actual={'missing'!r}"

    expr = assigns["result"]
    assert isinstance(expr, ast.BoolOp), f"expected={'BoolOp'!r} actual={type(expr).__name__!r}"
    assert isinstance(expr.op, ast.Or), f"expected={'Or'!r} actual={type(expr.op).__name__!r}"
    assert len(expr.values) == 2, f"expected={2!r} actual={len(expr.values)!r}"

    left, right = expr.values
    assert isinstance(left, ast.BoolOp), f"expected={'BoolOp'!r} actual={type(left).__name__!r}"
    assert isinstance(left.op, ast.And), f"expected={'And'!r} actual={type(left.op).__name__!r}"
    assert len(left.values) == 2, f"expected={2!r} actual={len(left.values)!r}"

    l0, l1 = left.values
    assert isinstance(l0, ast.UnaryOp), f"expected={'UnaryOp'!r} actual={type(l0).__name__!r}"
    assert isinstance(l0.op, ast.Not), f"expected={'Not'!r} actual={type(l0.op).__name__!r}"
    assert isinstance(l0.operand, ast.Name) and l0.operand.id == "A", f"expected={'A'!r} actual={ast.dump(l0.operand, include_attributes=False)!r}"
    assert isinstance(l1, ast.Name) and l1.id == "B", f"expected={'B'!r} actual={ast.dump(l1, include_attributes=False)!r}"
    assert isinstance(right, ast.Name) and right.id == "C", f"expected={'C'!r} actual={ast.dump(right, include_attributes=False)!r}"

    # Ensure print argument is exactly the name "result"
    print_arg = _find_print_arg(tree)
    assert isinstance(print_arg, ast.Name) and print_arg.id == "result", f"expected={'result'!r} actual={ast.dump(print_arg, include_attributes=False) if print_arg else None!r}"


def test_logic_matches_expression_for_all_combinations():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    A, B, C = mod.A, mod.B, mod.C
    expected = (not A and B) or C
    actual = mod.result
    assert actual == expected, f"expected={expected!r} actual={actual!r}"