import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

MODULE_FILENAME = "02_replaceLastItemNegativeIndex.py"
MODULE_NAME = "m02_replaceLastItemNegativeIndex"


def load_module_capture_stdout():
    spec = importlib.util.spec_from_file_location(
        MODULE_NAME, os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    )
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_words_list_replaced_last_item_and_printed_correctly():
    module, out = load_module_capture_stdout()
    assert hasattr(module, "words"), "expected 'words' variable to exist"
    expected = ["sun", "moon", "stars"]
    actual = module.words
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert out.strip() == repr(expected), f"expected={repr(expected)!r} actual={out.strip()!r}"


def test_uses_negative_index_assignment_in_source():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    if isinstance(target.value, ast.Name) and target.value.id == "words":
                        sl = target.slice
                        if isinstance(sl, ast.Constant) and isinstance(sl.value, int) and sl.value < 0:
                            found = True
                        elif isinstance(sl, ast.UnaryOp) and isinstance(sl.op, ast.USub) and isinstance(
                            sl.operand, ast.Constant
                        ):
                            if isinstance(sl.operand.value, int) and sl.operand.value > 0:
                                found = True
    assert found, f"expected={'negative index assignment to words[-1]'} actual={'not found'}"