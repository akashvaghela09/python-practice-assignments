import importlib.util
import io
import os
import contextlib
import sys
import pytest

MODULE_FILE = "05_nestedLenCounts.py"


def run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("mod_05_nestedLenCounts", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_stdout_exact():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    _, out = run_module_capture_stdout(path)
    expected = "3 6\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_computed_values_are_ints_and_correct():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    mod, _ = run_module_capture_stdout(path)

    expected_inner = len(mod.items)
    expected_total = sum(len(x) for x in mod.items)

    assert isinstance(mod.inner_count, int), f"expected={int!r} actual={type(mod.inner_count)!r}"
    assert isinstance(mod.total_count, int), f"expected={int!r} actual={type(mod.total_count)!r}"

    assert mod.inner_count == expected_inner, f"expected={expected_inner!r} actual={mod.inner_count!r}"
    assert mod.total_count == expected_total, f"expected={expected_total!r} actual={mod.total_count!r}"


def test_not_none():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    mod, _ = run_module_capture_stdout(path)

    expected = False
    actual_inner = mod.inner_count is None
    actual_total = mod.total_count is None

    assert actual_inner == expected, f"expected={expected!r} actual={actual_inner!r}"
    assert actual_total == expected, f"expected={expected!r} actual={actual_total!r}"


def test_counts_match_items_structure():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    mod, _ = run_module_capture_stdout(path)

    expected_inner = len(mod.items)
    expected_total = len([y for x in mod.items for y in x])

    assert mod.inner_count == expected_inner, f"expected={expected_inner!r} actual={mod.inner_count!r}"
    assert mod.total_count == expected_total, f"expected={expected_total!r} actual={mod.total_count!r}"