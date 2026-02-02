import importlib.util
import io
import os
import sys
import contextlib
import ast
import pytest

MODULE_FILE = "05_listAndTupleBasics.py"


def load_module(path):
    spec = importlib.util.spec_from_file_location("student_mod_05", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_script_capture_output(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        load_module(path)
    return buf.getvalue()


def test_script_prints_two_lines_exactly():
    out = run_script_capture_output(MODULE_FILE)
    lines = out.splitlines()
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    assert lines[0] == "<class 'list'>", f"expected={'<class \\'list\\'>'!r} actual={lines[0]!r}"
    assert lines[1] == "green", f"expected={'green'!r} actual={lines[1]!r}"


def test_colors_tuple_exists_is_tuple_and_matches_list():
    mod = load_module(MODULE_FILE)
    assert hasattr(mod, "colors_tuple"), f"expected={True!r} actual={False!r}"
    ct = mod.colors_tuple
    assert isinstance(ct, tuple), f"expected={tuple.__name__!r} actual={type(ct).__name__!r}"
    assert hasattr(mod, "colors_list"), f"expected={True!r} actual={False!r}"
    cl = mod.colors_list
    assert isinstance(cl, list), f"expected={list.__name__!r} actual={type(cl).__name__!r}"
    assert tuple(cl) == ct, f"expected={tuple(cl)!r} actual={ct!r}"
    assert len(ct) == 3, f"expected={3!r} actual={len(ct)!r}"


def test_source_contains_no_placeholder_assignment():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    bad_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "colors_tuple":
                    if isinstance(node.value, ast.Constant) and node.value.value is None:
                        bad_nodes.append(node)

    assert not bad_nodes, f"expected={0!r} actual={len(bad_nodes)!r}"


def test_no_input_is_used():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    assert "input(" not in src, f"expected={False!r} actual={True!r}"


@pytest.mark.parametrize("name", ["colors_list", "colors_tuple"])
def test_variables_are_not_modified_between_imports(name):
    mod1 = load_module(MODULE_FILE)
    mod2 = load_module(MODULE_FILE)
    v1 = getattr(mod1, name)
    v2 = getattr(mod2, name)
    assert v1 == v2, f"expected={v1!r} actual={v2!r}"