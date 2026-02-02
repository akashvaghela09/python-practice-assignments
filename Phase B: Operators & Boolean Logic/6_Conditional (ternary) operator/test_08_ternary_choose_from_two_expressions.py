import importlib
import io
import contextlib
import re
import ast

MODULE_NAME = "08_ternary_choose_from_two_expressions"


def run_module_capture_stdout():
    mod = importlib.import_module(MODULE_NAME)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return buf.getvalue()


def test_prints_expected_output_exactly(capsys):
    importlib.import_module(MODULE_NAME)
    captured = capsys.readouterr().out
    expected = "hours=1.5\n"
    assert captured == expected, f"expected={expected!r} actual={captured!r}"


def test_print_format_and_value_parses_to_expected_float():
    out = run_module_capture_stdout()
    m = re.fullmatch(r"hours=([^\n]+)\n", out)
    assert m is not None, f"expected={'match'} actual={out!r}"
    actual = float(m.group(1))
    expected = 1.5
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_conditional_expression_for_hours_assignment():
    mod = importlib.import_module(MODULE_NAME)
    src = open(mod.__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    hours_assign = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "hours":
                    hours_assign = node
                    break
        if hours_assign is not None:
            break

    assert hours_assign is not None, f"expected={'hours assignment'} actual={None!r}"
    is_ifexp = isinstance(hours_assign.value, ast.IfExp)
    assert is_ifexp, f"expected={'IfExp'} actual={type(hours_assign.value).__name__!r}"


def test_conditional_expression_branches_are_calculations_or_literals():
    mod = importlib.import_module(MODULE_NAME)
    src = open(mod.__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    hours_value = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "hours" for t in node.targets):
                hours_value = node.value
                break

    assert isinstance(hours_value, ast.IfExp), f"expected={'IfExp'} actual={type(hours_value).__name__!r}"

    def is_calc(node):
        return isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Call, ast.Constant, ast.Name, ast.Attribute))

    ok_body = is_calc(hours_value.body)
    ok_orelse = is_calc(hours_value.orelse)
    assert ok_body and ok_orelse, f"expected={(True, True)!r} actual={(ok_body, ok_orelse)!r}"


def test_condition_compares_minutes_to_60_with_greater_than():
    mod = importlib.import_module(MODULE_NAME)
    src = open(mod.__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    ifexp = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "hours" for t in node.targets):
            ifexp = node.value
            break

    assert isinstance(ifexp, ast.IfExp), f"expected={'IfExp'} actual={type(ifexp).__name__!r}"
    test = ifexp.test
    ok = (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "minutes"
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Gt)
        and len(test.comparators) == 1
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == 60
    )
    assert ok, f"expected={True!r} actual={ok!r}"