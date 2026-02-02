import importlib
import io
import contextlib
import pathlib
import re
import ast
import pytest

MODULE_NAME = "13_deduplicatePreserveOrder"


def _module_path():
    return pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"


def _load_source():
    p = _module_path()
    return p.read_text(encoding="utf-8")


def test_no_placeholder_remains():
    src = _load_source()
    assert "____" not in src, f"expected placeholder removed, actual present={('____' in src)}"


def test_printed_output_exact():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(MODULE_NAME)
    out = buf.getvalue()
    expected = "[3, 1, 2, 5, 4]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_result_variable_matches_printed_list():
    mod = importlib.import_module(MODULE_NAME)
    expected = [3, 1, 2, 5, 4]
    actual = getattr(mod, "result", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_seen_set_and_result_list_and_loop_present():
    src = _load_source()
    assert re.search(r"^\s*seen\s*=\s*set\(\)\s*$", src, re.M), f"expected={True!r} actual={bool(re.search(r'^\\s*seen\\s*=\\s*set\\(\\)\\s*$', src, re.M))!r}"
    assert re.search(r"^\s*result\s*=\s*\[\]\s*$", src, re.M), f"expected={True!r} actual={bool(re.search(r'^\\s*result\\s*=\\s*\\[\\]\\s*$', src, re.M))!r}"
    assert re.search(r"^\s*for\s+\w+\s+in\s+items\s*:\s*$", src, re.M), f"expected={True!r} actual={bool(re.search(r'^\\s*for\\s+\\w+\\s+in\\s+items\\s*:\\s*$', src, re.M))!r}"


def test_items_list_unchanged():
    mod = importlib.import_module(MODULE_NAME)
    expected = [3, 1, 3, 2, 1, 5, 2, 4, 5]
    actual = getattr(mod, "items", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_print_statement_prints_result():
    src = _load_source()
    tree = ast.parse(src)
    prints = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
    ]
    assert len(prints) == 1, f"expected={1!r} actual={len(prints)!r}"
    call = prints[0]
    arg0 = call.args[0] if call.args else None
    is_result = isinstance(arg0, ast.Name) and arg0.id == "result"
    assert is_result, f"expected={True!r} actual={is_result!r}"