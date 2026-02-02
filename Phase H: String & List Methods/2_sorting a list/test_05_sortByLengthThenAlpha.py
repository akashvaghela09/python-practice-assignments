import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

EXPECTED = ['an', 'to', 'ant', 'bee', 'zoo', 'apple']


def load_module(module_name="assignment_05"):
    path = os.path.join(os.path.dirname(__file__), "05_sortByLengthThenAlpha.py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def parse_last_list_from_output(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def test_words_sorted_in_module_variable():
    mod, _ = load_module("assignment_05_var")
    assert hasattr(mod, "words")
    actual = mod.words
    assert actual == EXPECTED, f"expected={EXPECTED} actual={actual}"


def test_printed_output_matches_expected_list():
    _, out = load_module("assignment_05_out")
    actual = parse_last_list_from_output(out)
    assert actual == EXPECTED, f"expected={EXPECTED} actual={actual}"


def test_words_is_list_of_strings():
    mod, _ = load_module("assignment_05_type")
    actual = mod.words
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    assert all(isinstance(x, str) for x in actual), f"expected={str} actual={set(type(x) for x in actual)}"
    assert actual == EXPECTED, f"expected={EXPECTED} actual={actual}"