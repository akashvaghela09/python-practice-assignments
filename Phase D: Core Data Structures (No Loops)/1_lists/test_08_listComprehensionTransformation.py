import ast
import importlib.util
import io
import os
import contextlib
import pytest

MODULE_FILE = "08_listComprehensionTransformation.py"


def load_module_from_path(tmp_path):
    src_path = tmp_path / MODULE_FILE
    spec = importlib.util.spec_from_file_location("m08_listComprehensionTransformation", str(src_path))
    mod = importlib.util.module_from_spec(spec)
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        spec.loader.exec_module(mod)
    return mod, f.getvalue()


def test_upper_words_is_correct_transformation(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src, "r", encoding="utf-8").read()
    (tmp_path / MODULE_FILE).write_text(code, encoding="utf-8")

    mod, _ = load_module_from_path(tmp_path)

    expected = [w.upper() for w in mod.words]
    actual = getattr(mod, "upper_words", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_list_comprehension_not_loop_or_map(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src, "r", encoding="utf-8").read()
    (tmp_path / MODULE_FILE).write_text(code, encoding="utf-8")

    tree = ast.parse(code)

    listcomp_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.ListComp)]
    for_nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))]
    map_calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "map"
    ]

    assert len(listcomp_nodes) >= 1, f"expected={'>=1 list comprehensions'} actual={len(listcomp_nodes)!r}"
    assert len(for_nodes) == 0, f"expected={0!r} actual={len(for_nodes)!r}"
    assert len(map_calls) == 0, f"expected={0!r} actual={len(map_calls)!r}"


def test_printed_output_matches_value(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src, "r", encoding="utf-8").read()
    (tmp_path / MODULE_FILE).write_text(code, encoding="utf-8")

    mod, out = load_module_from_path(tmp_path)

    expected_line = repr(getattr(mod, "upper_words", None))
    actual_line = out.strip().splitlines()[-1].strip() if out.strip().splitlines() else ""
    assert actual_line == expected_line, f"expected={expected_line!r} actual={actual_line!r}"