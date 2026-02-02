import importlib.util
import os
import sys
from pathlib import Path


def _load_module():
    test_dir = Path(__file__).resolve().parent
    file_path = test_dir / "01_sortAscendingBasics.py"
    assert file_path.exists()
    module_name = "assignment_01_sortAscendingBasics"
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_nums_sorted_in_place(capsys):
    module = _load_module()
    expected = [1, 2, 3, 4, 5]
    actual = getattr(module, "nums", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_printed_output_matches_sorted_list(capsys):
    _ = _load_module()
    out = capsys.readouterr().out.strip()
    expected = str([1, 2, 3, 4, 5])
    assert out == expected, f"expected={expected} actual={out}"


def test_nums_is_list_of_ints():
    module = _load_module()
    nums = getattr(module, "nums", None)
    assert isinstance(nums, list), f"expected={list} actual={type(nums)}"
    types = [type(x) for x in nums]
    assert all(t is int for t in types), f"expected={int} actual={types}"