import importlib.util
import os
import ast
import pytest

FILE_NAME = "08_zipAndPairing.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("student_mod_08", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_pairs(mod):
    return [f"{l}:{n}" for l, n in zip(mod.letters, mod.nums)]


def test_module_imports():
    _load_module()


def test_pairs_is_list():
    mod = _load_module()
    assert isinstance(mod.pairs, list), f"expected=list actual={type(mod.pairs).__name__}"


def test_pairs_matches_zip_format():
    mod = _load_module()
    expected = _expected_pairs(mod)
    assert mod.pairs == expected, f"expected={expected} actual={mod.pairs}"


def test_pairs_content_types_are_strings():
    mod = _load_module()
    actual_types = [type(x).__name__ for x in mod.pairs]
    expected_types = ["str"] * len(mod.pairs)
    assert actual_types == expected_types, f"expected={expected_types} actual={actual_types}"


def test_pairs_length_matches_inputs():
    mod = _load_module()
    expected_len = min(len(mod.letters), len(mod.nums))
    actual_len = len(mod.pairs)
    assert actual_len == expected_len, f"expected={expected_len} actual={actual_len}"


def test_uses_zip_in_source():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    used_zip = any(isinstance(c.func, ast.Name) and c.func.id == "zip" for c in calls)
    assert used_zip is True, f"expected={True} actual={used_zip}"