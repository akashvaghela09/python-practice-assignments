import importlib.util
import io
import os
import sys
import ast
import contextlib
import pytest

FILE_NAME = "03_sortedDoesNotMutate.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("mod_03_sortedDoesNotMutate", path)
    module = importlib.util.module_from_spec(spec)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        spec.loader.exec_module(module)
    return module, stdout.getvalue()


def _parse_printed_lists(output):
    lines = [line.strip() for line in output.splitlines() if line.strip() != ""]
    assert len(lines) >= 2, f"expected={2} actual={len(lines)}"
    a = ast.literal_eval(lines[-2])
    b = ast.literal_eval(lines[-1])
    return a, b


def test_printed_outputs_are_expected_lists():
    _, out = _load_module()
    printed_original, printed_new = _parse_printed_lists(out)

    exp_original = [3, 1, 2]
    exp_new = [1, 2, 3]

    assert printed_original == exp_original, f"expected={exp_original} actual={printed_original}"
    assert printed_new == exp_new, f"expected={exp_new} actual={printed_new}"


def test_original_not_mutated_and_new_list_sorted():
    mod, _ = _load_module()

    assert hasattr(mod, "original"), "expected=True actual=False"
    assert hasattr(mod, "new_list"), "expected=True actual=False"

    exp_original = [3, 1, 2]
    exp_new = [1, 2, 3]

    assert mod.original == exp_original, f"expected={exp_original} actual={mod.original}"
    assert mod.new_list == exp_new, f"expected={exp_new} actual={mod.new_list}"
    assert mod.new_list is not mod.original, f"expected={'different_objects'} actual={'same_object' if mod.new_list is mod.original else 'different_objects'}"


def test_new_list_matches_sorted_original_and_original_unchanged_after_sorting_reference():
    mod, _ = _load_module()

    exp_original = [3, 1, 2]
    exp_sorted = sorted(exp_original)

    assert mod.original == exp_original, f"expected={exp_original} actual={mod.original}"
    assert mod.new_list == exp_sorted, f"expected={exp_sorted} actual={mod.new_list}"