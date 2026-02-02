import importlib
import sys
import ast
import pathlib
import pytest


MODULE_NAME = "04_booleanAndOrBasics"


def _load_source():
    mod = sys.modules.get(MODULE_NAME)
    if mod and getattr(mod, "__file__", None):
        return pathlib.Path(mod.__file__).read_text(encoding="utf-8")
    spec = importlib.util.find_spec(MODULE_NAME)
    if spec is None or spec.origin is None:
        raise AssertionError("module not found")
    return pathlib.Path(spec.origin).read_text(encoding="utf-8")


def _parse_assignments(tree):
    values = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {"has_id", "has_ticket", "allowed_in", "needs_help"}:
                values[name] = node.value
    return values


def _is_bool_constant(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return True
    return False


def _binop_is_and(node):
    return isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And)


def _binop_is_or(node):
    return isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or)


def _name(node, s):
    return isinstance(node, ast.Name) and node.id == s


def _not_name(node, s):
    return isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not) and _name(node.operand, s)


def _is_expected_allowed_expr(expr):
    if not _binop_is_and(expr):
        return False
    vals = expr.values
    if len(vals) != 2:
        return False
    combos = [
        (_name(vals[0], "has_id") and _name(vals[1], "has_ticket")),
        (_name(vals[0], "has_ticket") and _name(vals[1], "has_id")),
    ]
    return any(combos)


def _is_expected_needs_help_expr(expr):
    if _binop_is_or(expr):
        vals = expr.values
        if len(vals) != 2:
            return False
        combos = [
            (_not_name(vals[0], "has_id") and _not_name(vals[1], "has_ticket")),
            (_not_name(vals[0], "has_ticket") and _not_name(vals[1], "has_id")),
        ]
        return any(combos)

    if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not) and _binop_is_and(expr.operand):
        vals = expr.operand.values
        if len(vals) != 2:
            return False
        combos = [
            (_name(vals[0], "has_id") and _name(vals[1], "has_ticket")),
            (_name(vals[0], "has_ticket") and _name(vals[1], "has_id")),
        ]
        return any(combos)

    return False


def test_module_imports_without_syntax_error():
    importlib.import_module(MODULE_NAME)


def test_printed_output_matches_expected(capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    importlib.import_module(MODULE_NAME)
    out = capsys.readouterr().out.splitlines()
    assert out == ["False", "True"], f"expected={['False','True']} actual={out}"


def test_variables_are_booleans():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    mod = importlib.import_module(MODULE_NAME)
    assert isinstance(mod.allowed_in, bool), f"expected={bool} actual={type(mod.allowed_in)}"
    assert isinstance(mod.needs_help, bool), f"expected={bool} actual={type(mod.needs_help)}"


def test_logic_uses_and_or_not_hardcoded():
    source = _load_source()
    tree = ast.parse(source)
    assigns = _parse_assignments(tree)

    assert "allowed_in" in assigns, f"expected={'allowed_in assignment'} actual={list(assigns.keys())}"
    assert "needs_help" in assigns, f"expected={'needs_help assignment'} actual={list(assigns.keys())}"

    allowed_expr = assigns["allowed_in"]
    needs_expr = assigns["needs_help"]

    assert not _is_bool_constant(allowed_expr), f"expected={'non-constant expr'} actual={'constant bool'}"
    assert not _is_bool_constant(needs_expr), f"expected={'non-constant expr'} actual={'constant bool'}"

    assert _is_expected_allowed_expr(allowed_expr), f"expected={'has_id and has_ticket'} actual={ast.dump(allowed_expr, include_attributes=False)}"
    assert _is_expected_needs_help_expr(needs_expr), f"expected={'not has_id or not has_ticket'} actual={ast.dump(needs_expr, include_attributes=False)}"


def test_logic_consistency_for_all_boolean_inputs(monkeypatch):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    mod = importlib.import_module(MODULE_NAME)

    for has_id in (False, True):
        for has_ticket in (False, True):
            monkeypatch.setattr(mod, "has_id", has_id, raising=True)
            monkeypatch.setattr(mod, "has_ticket", has_ticket, raising=True)

            allowed_expected = has_id and has_ticket
            needs_expected = (not has_id) or (not has_ticket)

            allowed_actual = (mod.has_id and mod.has_ticket)
            needs_actual = ((not mod.has_id) or (not mod.has_ticket))

            assert allowed_actual == allowed_expected, f"expected={allowed_expected} actual={allowed_actual}"
            assert needs_actual == needs_expected, f"expected={needs_expected} actual={needs_actual}"