import importlib
import io
import sys
import types
import pytest

MODULE_NAME = "06_breakOnTarget"


def load_module_fresh():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def get_output():
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        load_module_fresh()
    finally:
        sys.stdout = old
    return buf.getvalue().splitlines()


def test_expected_exact_output_lines():
    expected = [
        "checking 3",
        "checking 7",
        "checking 0",
        "found 0 at index 2",
    ]
    actual = get_output()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_stops_at_first_zero_only():
    lines = get_output()
    assert lines.count("checking 0") == 1, f"expected={1!r} actual={lines.count('checking 0')!r}"
    assert all("found 0 at index" in line for line in lines if line.startswith("found")), f"expected={True!r} actual={any(line.startswith('found') and 'found 0 at index' not in line for line in lines)!r}"
    assert all("checking 9" not in line for line in lines), f"expected={False!r} actual={any('checking 9' in line for line in lines)!r}"


def test_print_format_two_tokens_for_checking_lines():
    lines = get_output()
    checking = [ln for ln in lines if ln.startswith("checking ")]
    assert len(checking) == 3, f"expected={3!r} actual={len(checking)!r}"
    split_counts = [len(ln.split()) for ln in checking]
    assert all(c == 2 for c in split_counts), f"expected={True!r} actual={split_counts!r}"