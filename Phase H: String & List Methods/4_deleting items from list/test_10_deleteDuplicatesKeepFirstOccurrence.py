import importlib.util
import os
import sys
from types import ModuleType


def _load_module():
    filename = "10_deleteDuplicatesKeepFirstOccurrence.py"
    module_name = "deleteDuplicatesKeepFirstOccurrence_10"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _expected_unique_keep_first(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def test_nums_removed_duplicates_in_place_keep_first():
    m = _load_module()
    original = [2, 1, 2, 3, 1, 4, 3]
    expected = _expected_unique_keep_first(original)
    actual = getattr(m, "nums", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_nums_is_list_and_length_matches_expected():
    m = _load_module()
    original = [2, 1, 2, 3, 1, 4, 3]
    expected = _expected_unique_keep_first(original)
    actual = getattr(m, "nums", None)
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    assert len(actual) == len(expected), f"expected={len(expected)} actual={len(actual)}"


def test_no_duplicates_remain_and_order_is_first_occurrence():
    m = _load_module()
    original = [2, 1, 2, 3, 1, 4, 3]
    expected = _expected_unique_keep_first(original)
    actual = getattr(m, "nums", None)
    assert len(actual) == len(set(actual)), f"expected={len(set(actual))} actual={len(actual)}"
    assert actual == expected, f"expected={expected} actual={actual}"


def test_global_list_object_mutated_not_reassigned():
    m = _load_module()
    path = os.path.join(os.path.dirname(__file__), "10_deleteDuplicatesKeepFirstOccurrence.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    original = [2, 1, 2, 3, 1, 4, 3]
    expected = _expected_unique_keep_first(original)
    actual = getattr(m, "nums", None)

    # If student did in-place deletions, there should be no assignment to nums after initialization.
    # This is a best-effort heuristic to catch `nums = [...]` reassignment solutions.
    init_idx = src.find("nums =")
    later_assign_idx = src.find("nums =", init_idx + 1) if init_idx != -1 else -1
    assert later_assign_idx == -1, f"expected={-1} actual={later_assign_idx}"

    assert actual == expected, f"expected={expected} actual={actual}"