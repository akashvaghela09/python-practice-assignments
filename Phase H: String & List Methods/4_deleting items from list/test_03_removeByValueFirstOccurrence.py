import importlib.util
import io
import os
import sys
import ast
import pytest

MODULE_FILENAME = "03_removeByValueFirstOccurrence.py"


def load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout
    return mod, captured.getvalue(), dst.read_text(encoding="utf-8")


def parse_printed_colors(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    assert lines, f"expected={True} actual={False}"
    line = lines[-1]
    assert line.startswith("colors:"), f"expected={'colors:'} actual={line.split(':')[0] + ':' if ':' in line else line}"
    rhs = line[len("colors:"):].strip()
    try:
        val = ast.literal_eval(rhs)
    except Exception:
        val = None
    assert isinstance(val, list), f"expected={list} actual={type(val)}"
    return val


def test_colors_list_value_after_execution(tmp_path):
    mod, out, _ = load_module(tmp_path)
    expected = ["blue", "red", "green"]
    actual = getattr(mod, "colors", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_colors(tmp_path):
    mod, out, _ = load_module(tmp_path)
    printed = parse_printed_colors(out)
    actual = getattr(mod, "colors", None)
    assert printed == actual, f"expected={actual} actual={printed}"


def test_first_occurrence_removed_only(tmp_path):
    mod, _, _ = load_module(tmp_path)
    colors = getattr(mod, "colors", None)
    expected = ["blue", "red", "green"]
    assert colors == expected, f"expected={expected} actual={colors}"
    assert colors.count("red") == 1, f"expected={1} actual={colors.count('red')}"


def test_uses_remove_method_in_source(tmp_path):
    _, _, src = load_module(tmp_path)
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    has_remove_call = any(
        isinstance(c.func, ast.Attribute) and c.func.attr == "remove"
        for c in calls
    )
    assert has_remove_call, f"expected={True} actual={False}"


def test_not_using_pop_or_del_for_removal(tmp_path):
    _, _, src = load_module(tmp_path)
    tree = ast.parse(src)

    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    has_pop_call = any(
        isinstance(c.func, ast.Attribute) and c.func.attr == "pop"
        for c in calls
    )

    has_del = any(isinstance(n, ast.Delete) for n in ast.walk(tree))

    assert has_pop_call is False, f"expected={False} actual={True}"
    assert has_del is False, f"expected={False} actual={True}"