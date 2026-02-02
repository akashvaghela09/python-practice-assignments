import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_NAME = "07_setUniqueness"
FILE_NAME = "07_setUniqueness.py"


def _load_module_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)

    stdout = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout

    return module, stdout.getvalue()


def test_prints_single_line_exact():
    _, out = _load_module_capture_stdout()
    expected = "4\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_unique_items_is_set_and_matches_items_dedup():
    module, _ = _load_module_capture_stdout()
    assert hasattr(module, "unique_items"), "expected=True actual=False"
    assert isinstance(module.unique_items, set), f"expected={set!r} actual={type(module.unique_items)!r}"

    expected_set = set(module.items)
    actual_set = module.unique_items
    assert actual_set == expected_set, f"expected={expected_set!r} actual={actual_set!r}"


def test_unique_items_length_correct():
    module, _ = _load_module_capture_stdout()
    expected_len = len(set(module.items))
    actual_len = len(module.unique_items)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"