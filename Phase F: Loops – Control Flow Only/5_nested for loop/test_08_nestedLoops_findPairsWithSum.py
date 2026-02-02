import importlib.util
import os
import sys


def _load_module():
    fname = "08_nestedLoops_findPairsWithSum.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("m08_nestedLoops_findPairsWithSum", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_pairs_is_defined_and_is_list():
    mod = _load_module()
    assert hasattr(mod, "pairs")
    assert isinstance(mod.pairs, list), f"expected={list} actual={type(mod.pairs)}"


def test_pairs_matches_expected_indices_for_given_input():
    mod = _load_module()
    expected = [(0, 3), (1, 2)]
    assert mod.pairs == expected, f"expected={expected} actual={mod.pairs}"


def test_pairs_contains_valid_unique_ordered_index_pairs():
    mod = _load_module()
    nums = getattr(mod, "nums")
    target = getattr(mod, "target")
    pairs = getattr(mod, "pairs")

    seen = set()
    for p in pairs:
        assert isinstance(p, tuple), f"expected={tuple} actual={type(p)}"
        assert len(p) == 2, f"expected={2} actual={len(p)}"
        i, j = p
        assert isinstance(i, int), f"expected={int} actual={type(i)}"
        assert isinstance(j, int), f"expected={int} actual={type(j)}"
        assert 0 <= i < len(nums), f"expected={[0, len(nums) - 1]} actual={i}"
        assert 0 <= j < len(nums), f"expected={[0, len(nums) - 1]} actual={j}"
        assert i < j, f"expected={'i<j'} actual={(i, j)}"
        assert (i, j) not in seen, f"expected={'unique'} actual={(i, j)}"
        seen.add((i, j))
        assert nums[i] + nums[j] == target, f"expected={target} actual={nums[i] + nums[j]}"


def test_pairs_are_exhaustive_for_given_nums_target():
    mod = _load_module()
    nums = mod.nums
    target = mod.target

    expected_set = set()
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                expected_set.add((i, j))

    actual_set = set(mod.pairs)
    assert actual_set == expected_set, f"expected={sorted(expected_set)} actual={sorted(actual_set)}"