import importlib.util
import os
import sys
import pytest


def _load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_student_module(capsys):
    here = os.path.dirname(__file__)
    path = os.path.join(here, "07_indexLoopWithRangeLen.py")
    assert os.path.exists(path), f"expected={True} actual={os.path.exists(path)}"
    name = "student_07_indexLoopWithRangeLen"
    if name in sys.modules:
        del sys.modules[name]
    _load_module_from_path(path, name)
    out = capsys.readouterr().out
    return out


def test_prints_all_items_with_indices(capsys):
    out = _run_student_module(capsys)
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    expected = [f"{i}:{ch}" for i, ch in enumerate(["a", "b", "c", "d"])]
    assert lines == expected, f"expected={expected} actual={lines}"


def test_output_has_exact_line_count(capsys):
    out = _run_student_module(capsys)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    expected_count = 4
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count} actual={actual_count}"


def test_each_line_format_index_colon_item(capsys):
    out = _run_student_module(capsys)
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    actual_pairs = []
    for ln in lines:
        parts = ln.split(":", 1)
        if len(parts) != 2:
            actual_pairs.append(("INVALID", ln))
            continue
        left, right = parts[0], parts[1]
        actual_pairs.append((left, right))
    expected_pairs = [(str(i), v) for i, v in enumerate(["a", "b", "c", "d"])]
    assert actual_pairs == expected_pairs, f"expected={expected_pairs} actual={actual_pairs}"


def test_no_extra_characters_or_spaces(capsys):
    out = _run_student_module(capsys)
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    expected = [f"{i}:{ch}" for i, ch in enumerate(["a", "b", "c", "d"])]
    actual = lines
    assert actual == expected, f"expected={expected} actual={actual}"


def test_runs_without_syntax_error():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "07_indexLoopWithRangeLen.py")
    assert os.path.exists(path), f"expected={True} actual={os.path.exists(path)}"
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        compile(src, path, "exec")
        ok = True
    except SyntaxError:
        ok = False
    assert ok is True, f"expected={True} actual={ok}"