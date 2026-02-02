import ast
import importlib.util
import io
import os
import sys


def _import_module_from_filename(filename):
    module_name = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_file_capture_stdout(filepath):
    old_stdout = sys.stdout
    try:
        buf = io.StringIO()
        sys.stdout = buf
        _import_module_from_filename(filepath)
        return buf.getvalue()
    finally:
        sys.stdout = old_stdout


def test_prints_expected_list():
    filepath = os.path.join(os.path.dirname(__file__), "01_splitWordsBasics.py")
    out = _run_file_capture_stdout(filepath).strip()
    expected = str(["Python", "is", "fun"])
    assert out == expected, f"expected={expected} actual={out}"


def test_words_variable_is_list_of_words():
    filepath = os.path.join(os.path.dirname(__file__), "01_splitWordsBasics.py")
    mod = _import_module_from_filename(filepath)
    expected = ["Python", "is", "fun"]
    assert getattr(mod, "words", None) == expected, f"expected={expected} actual={getattr(mod, 'words', None)}"
    assert isinstance(getattr(mod, "words", None), list), f"expected={list} actual={type(getattr(mod, 'words', None))}"


def test_uses_split_method_call():
    filepath = os.path.join(os.path.dirname(__file__), "01_splitWordsBasics.py")
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    split_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "split":
            split_calls.append(node)

    assert len(split_calls) >= 1, f"expected>={1} actual={len(split_calls)}"