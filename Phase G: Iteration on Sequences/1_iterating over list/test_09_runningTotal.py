import ast
import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

import pytest


MODULE_FILE = "09_runningTotal.py"


def _load_module_from_path(path, name="student_module_09"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected_running(nums):
    running = []
    total = 0
    for n in nums:
        total += n
        running.append(total)
    return running


def _extract_first_list_literal(s):
    m = re.search(r"\[[^\]]*\]", s, flags=re.S)
    if not m:
        return None
    try:
        return ast.literal_eval(m.group(0))
    except Exception:
        return None


def test_script_runs_and_prints_running_total(capsys):
    path = os.path.join(os.getcwd(), MODULE_FILE)
    assert os.path.exists(path)

    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = _load_module_from_path(path)

    out = buf.getvalue().strip()
    printed_list = _extract_first_list_literal(out)
    assert printed_list is not None

    nums = getattr(mod, "nums", None)
    assert isinstance(nums, list)

    expected = _expected_running(nums)
    assert printed_list == expected, f"expected={expected} actual={printed_list}"


def test_running_variable_exists_and_correct(capsys):
    path = os.path.join(os.getcwd(), MODULE_FILE)
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = _load_module_from_path(path, name="student_module_09_b")

    nums = getattr(mod, "nums", None)
    assert isinstance(nums, list)

    running = getattr(mod, "running", None)
    assert isinstance(running, list)

    expected = _expected_running(nums)
    assert running == expected, f"expected={expected} actual={running}"


def test_total_variable_final_value(capsys):
    path = os.path.join(os.getcwd(), MODULE_FILE)
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = _load_module_from_path(path, name="student_module_09_c")

    nums = getattr(mod, "nums", None)
    assert isinstance(nums, list)

    total = getattr(mod, "total", None)
    assert isinstance(total, int)

    expected_total = sum(nums)
    assert total == expected_total, f"expected={expected_total} actual={total}"


def test_uses_loop_construct():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    has_for = any(isinstance(node, ast.For) for node in ast.walk(tree))
    assert has_for

    has_augassign_or_add = any(
        isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add)
        for node in ast.walk(tree)
    ) or any(
        isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add)
        for node in ast.walk(tree)
    )
    assert has_augassign_or_add

    has_append_call = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "append"
        for node in ast.walk(tree)
    )
    assert has_append_call