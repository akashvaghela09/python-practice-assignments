import importlib
import ast
import io
import contextlib
import os
import sys

MODULE_NAME = "02_sortDescendingBasics"


def _import_fresh():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def _run_and_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _import_fresh()
    return mod, buf.getvalue()


def test_nums_sorted_descending_and_contains_same_elements():
    mod, _ = _run_and_capture_stdout()
    actual = getattr(mod, "nums", None)
    expected = sorted([1, 9, 3, 7, 5], reverse=True)
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    assert actual == expected, f"expected={expected} actual={actual}"


def test_stdout_prints_final_nums_list():
    mod, out = _run_and_capture_stdout()
    actual_nums = getattr(mod, "nums", None)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    actual_last_line = lines[-1] if lines else None
    expected_last_line = repr(actual_nums)
    assert actual_last_line == expected_last_line, f"expected={expected_last_line} actual={actual_last_line}"


def test_source_does_not_hardcode_target_list_literal_for_nums_assignment():
    mod = _import_fresh()
    path = getattr(mod, "__file__", None)
    assert path and os.path.exists(path), f"expected={True} actual={bool(path and os.path.exists(path))}"

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    target_literal = ast.List(elts=[ast.Constant(9), ast.Constant(7), ast.Constant(5), ast.Constant(3), ast.Constant(1)], ctx=ast.Load())

    def is_target_list(node):
        return (
            isinstance(node, ast.List)
            and len(node.elts) == 5
            and all(isinstance(e, ast.Constant) for e in node.elts)
            and [e.value for e in node.elts] == [9, 7, 5, 3, 1]
        )

    hardcoded = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "nums" and is_target_list(node.value):
                    hardcoded = True
        if isinstance(node, ast.AnnAssign):
            tgt = node.target
            if isinstance(tgt, ast.Name) and tgt.id == "nums" and node.value is not None and is_target_list(node.value):
                hardcoded = True

    assert hardcoded is False, f"expected={False} actual={hardcoded}"