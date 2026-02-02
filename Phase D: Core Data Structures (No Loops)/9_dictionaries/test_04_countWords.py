import importlib.util
import pathlib
import ast
import re

FILE_NAME = "04_countWords.py"


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location("countWords04", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _parse_printed_dict(text):
    s = text.strip()
    try:
        v = ast.literal_eval(s)
        return v if isinstance(v, dict) else None
    except Exception:
        return None


def test_counts_variable_is_correct():
    mod = _load_module()
    expected = {"red": 2, "blue": 1, "green": 2}
    actual = getattr(mod, "counts", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_counts(capsys):
    mod = _load_module()
    captured = capsys.readouterr()
    printed = captured.out.strip()
    actual_printed = _parse_printed_dict(printed)

    expected = {"red": 2, "blue": 1, "green": 2}
    actual_counts = getattr(mod, "counts", None)

    assert actual_printed == expected, f"expected={expected} actual={actual_printed}"
    assert actual_printed == actual_counts, f"expected={actual_counts} actual={actual_printed}"


def test_no_pass_left_in_loop_body():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    src = path.read_text(encoding="utf-8")

    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            has_pass = any(isinstance(stmt, ast.Pass) for stmt in node.body)
            assert not has_pass, f"expected={False} actual={has_pass}"


def test_counts_is_plain_dict():
    mod = _load_module()
    actual = getattr(mod, "counts", None)
    expected_type = dict
    assert type(actual) is expected_type, f"expected={expected_type} actual={type(actual)}"