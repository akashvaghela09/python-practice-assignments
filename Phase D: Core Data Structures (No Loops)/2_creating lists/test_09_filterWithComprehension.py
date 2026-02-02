import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


EXPECTED = ["tiger", "zebra", "giraffe"]


def load_module():
    filename = "09_filterWithComprehension.py"
    spec = importlib.util.spec_from_file_location("mod09_filterWithComprehension", os.path.join(os.getcwd(), filename))
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_long_words_value():
    module, _ = load_module()
    assert hasattr(module, "long_words")
    actual = module.long_words
    assert actual == EXPECTED, f"expected={EXPECTED} actual={actual}"


def test_printed_output_matches_long_words():
    module, out = load_module()
    printed = out.strip().splitlines()[-1] if out.strip() else ""
    try:
        printed_val = ast.literal_eval(printed)
    except Exception:
        printed_val = printed
    actual = module.long_words
    assert printed_val == actual, f"expected={actual} actual={printed_val}"


def test_long_words_is_list_of_strings():
    module, _ = load_module()
    actual = module.long_words
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    assert all(isinstance(x, str) for x in actual), f"expected={True} actual={all(isinstance(x, str) for x in actual)}"


def test_uses_list_comprehension_for_long_words():
    filename = "09_filterWithComprehension.py"
    with open(filename, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    target_assign = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "long_words":
                    target_assign = node
                    break
        if target_assign:
            break

    assert target_assign is not None, f"expected={True} actual={False}"
    is_listcomp = isinstance(target_assign.value, ast.ListComp)
    assert is_listcomp, f"expected={True} actual={is_listcomp}"


def test_filters_by_length_at_least_5():
    module, _ = load_module()
    actual = module.long_words
    cond = all(len(w) >= 5 for w in actual)
    assert cond, f"expected={True} actual={cond}"