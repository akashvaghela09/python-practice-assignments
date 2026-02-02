import ast
import importlib.util
import os
import pathlib
import sys
import types
import pytest


MODULE_FILENAME = "09_wordFrequencies.py"


def _load_module_from_path(path):
    name = "mod_09_wordFrequencies_under_test"
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _get_target_path():
    here = pathlib.Path(__file__).resolve()
    candidates = [
        pathlib.Path.cwd() / MODULE_FILENAME,
        here.parent / MODULE_FILENAME,
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]


def test_file_exists():
    path = _get_target_path()
    assert path.exists()


def test_module_is_valid_python():
    path = _get_target_path()
    source = path.read_text(encoding="utf-8")
    ast.parse(source)


def test_counts_output_expected(capsys):
    path = _get_target_path()
    module = _load_module_from_path(path)
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) >= 1
    last = out[-1].strip()
    expected = {"to": 3, "be": 2, "or": 1}
    try:
        actual = ast.literal_eval(last)
    except Exception:
        pytest.fail(f"expected={expected} actual={last}")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_counts_variable_is_correct(capsys):
    path = _get_target_path()
    module = _load_module_from_path(path)
    _ = capsys.readouterr()
    expected = {"to": 3, "be": 2, "or": 1}
    assert hasattr(module, "counts")
    actual = getattr(module, "counts")
    assert actual == expected, f"expected={expected} actual={actual}"


def test_counts_is_built_from_lower_split(capsys):
    path = _get_target_path()
    module = _load_module_from_path(path)
    _ = capsys.readouterr()
    expected_words = "To be or to be to".lower().split()
    assert hasattr(module, "words")
    actual_words = getattr(module, "words")
    assert actual_words == expected_words, f"expected={expected_words} actual={actual_words}"


def test_uses_for_loop_in_source():
    path = _get_target_path()
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_nodes) >= 1

    has_counts_subscript = any(
        isinstance(n, ast.Subscript) and isinstance(getattr(n, "value", None), ast.Name) and n.value.id == "counts"
        for n in ast.walk(tree)
    )
    assert has_counts_subscript is True