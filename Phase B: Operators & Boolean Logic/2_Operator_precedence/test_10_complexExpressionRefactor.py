import ast
import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

MODULE_FILENAME = "10_complexExpressionRefactor.py"


def _load_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_10", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _get_source():
    here = os.path.dirname(__file__)
    path = os.path.join(here, MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        return path, f.read()


def test_prints_exactly_one_with_newline():
    path, _ = _get_source()
    _, out = _load_module_capture_stdout(path)
    expected = "1\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_value_is_int_one_after_execution():
    path, _ = _get_source()
    mod, _ = _load_module_capture_stdout(path)
    expected = 1
    actual = getattr(mod, "value", None)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, int)


def test_second_assignment_is_expression_without_placeholders():
    _, src = _get_source()
    tree = ast.parse(src)
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    assert len(assigns) >= 2
    second = assigns[1]
    assert len(second.targets) == 1
    assert isinstance(second.targets[0], ast.Name) and second.targets[0].id == "value"
    assert not isinstance(second.value, ast.Name) or second.value.id != "__"
    assert "__" not in src


def test_only_parentheses_added_numbers_and_operators_unchanged():
    _, src = _get_source()
    lines = src.splitlines()
    first_line = None
    second_line = None
    for line in lines:
        if re.match(r"^\s*value\s*=", line):
            if first_line is None:
                first_line = line
            elif second_line is None:
                second_line = line
                break
    assert first_line is not None and second_line is not None

    def normalize(expr_line):
        s = expr_line.split("=", 1)[1].strip()
        s = s.split("#", 1)[0].strip()
        return s

    original = normalize(first_line)
    modified = normalize(second_line)

    def strip_parens_spaces(s):
        return re.sub(r"[()\s]", "", s)

    expected = strip_parens_spaces(original)
    actual = strip_parens_spaces(modified)
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


def test_uses_only_existing_numbers_and_operators():
    _, src = _get_source()
    tree = ast.parse(src)
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    second = assigns[1]
    nums = []

    def walk(node):
        for child in ast.walk(node):
            if isinstance(child, ast.Constant) and isinstance(child.value, (int, float)):
                nums.append(child.value)

    walk(second.value)
    expected_nums = sorted([8, 3, 2, 2, 3, 1])
    actual_nums = sorted(nums)
    assert expected_nums == actual_nums, f"expected={expected_nums!r} actual={actual_nums!r}"

    ops = set(type(n).__name__ for n in ast.walk(second.value) if isinstance(n, (ast.BinOp, ast.UnaryOp)))
    binops = [type(n.op).__name__ for n in ast.walk(second.value) if isinstance(n, ast.BinOp)]
    expected_binops = sorted(["Sub", "Mult", "Pow", "FloorDiv", "Add"])
    actual_binops = sorted(set(binops))
    assert expected_binops == actual_binops, f"expected={expected_binops!r} actual={actual_binops!r}"