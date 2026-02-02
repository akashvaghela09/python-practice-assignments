import importlib
import ast
import sys
import pytest


MODULE_NAME = "08_truthTableRows"


def _import_module():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def test_printed_output_exact(capsys):
    _import_module()
    out = capsys.readouterr().out
    expected = "row1: True\nrow2: False\nrow3: True\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_defined_and_boolean():
    m = _import_module()
    for name in ("A1", "B1", "row1", "A2", "B2", "row2", "A3", "B3", "row3"):
        assert hasattr(m, name), f"expected={True!r} actual={False!r}"
        val = getattr(m, name)
        assert isinstance(val, bool), f"expected={bool!r} actual={type(val)!r}"


def test_expr_values_match_xor_for_each_row():
    m = _import_module()

    def expr(a, b):
        return (a and (not b)) or ((not a) and b)

    expected_row1 = expr(m.A1, m.B1)
    expected_row2 = expr(m.A2, m.B2)
    expected_row3 = expr(m.A3, m.B3)

    assert m.row1 == expected_row1, f"expected={expected_row1!r} actual={m.row1!r}"
    assert m.row2 == expected_row2, f"expected={expected_row2!r} actual={m.row2!r}"
    assert m.row3 == expected_row3, f"expected={expected_row3!r} actual={m.row3!r}"


def test_source_has_no_placeholders():
    path = MODULE_NAME + ".py"
    src = open(path, "r", encoding="utf-8").read()
    assert "???" not in src, f"expected={False!r} actual={True!r}"


def test_no_input_calls_in_source():
    path = MODULE_NAME + ".py"
    src = open(path, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.found = False

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "input":
                self.found = True
            self.generic_visit(node)

    v = Visitor()
    v.visit(tree)
    assert v.found is False, f"expected={False!r} actual={v.found!r}"