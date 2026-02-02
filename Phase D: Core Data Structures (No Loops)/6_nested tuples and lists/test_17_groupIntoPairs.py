import ast
import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "17_groupIntoPairs.py"


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("groupIntoPairs_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_file_capture_stdout(path):
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        _load_module_from_path(path)
    finally:
        sys.stdout = old
    return buf.getvalue()


def _get_assignment_ast_value(code, name):
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
    return None


def _extract_list_constant(node):
    if not isinstance(node, ast.List):
        return None
    vals = []
    for elt in node.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, int):
            vals.append(elt.value)
        else:
            return None
    return vals


def _expected_pairs_from_nums(nums):
    if len(nums) % 2 != 0:
        raise ValueError("nums length must be even")
    return [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]


@pytest.fixture(scope="module")
def target_path():
    here = os.path.dirname(__file__)
    path = os.path.join(here, MODULE_FILENAME)
    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), MODULE_FILENAME)
    return path


@pytest.fixture(scope="module")
def source_text(target_path):
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def nums_from_source(source_text):
    node = _get_assignment_ast_value(source_text, "nums")
    nums = _extract_list_constant(node)
    if nums is None:
        pytest.skip("nums not a simple list constant; skipping derived expectation checks")
    return nums


def test_prints_expected_pairs(target_path, nums_from_source):
    out = _run_file_capture_stdout(target_path)
    actual_line = out.splitlines()[-1] if out.splitlines() else out
    expected_line = str(_expected_pairs_from_nums(nums_from_source))
    assert actual_line == expected_line, f"expected={expected_line!r} actual={actual_line!r}"


def test_pairs_variable_is_list_of_2_tuples(target_path, nums_from_source):
    mod = _load_module_from_path(target_path)
    assert hasattr(mod, "pairs")
    pairs = mod.pairs
    expected = _expected_pairs_from_nums(nums_from_source)
    assert isinstance(pairs, list), f"expected={type(expected).__name__} actual={type(pairs).__name__}"
    assert len(pairs) == len(expected), f"expected={len(expected)!r} actual={len(pairs)!r}"
    for idx, item in enumerate(pairs):
        assert isinstance(item, tuple), f"expected={tuple.__name__!r} actual={type(item).__name__!r}"
        assert len(item) == 2, f"expected={2!r} actual={len(item)!r}"
        exp_item = expected[idx]
        assert item == exp_item, f"expected={exp_item!r} actual={item!r}"


def test_no_none_pairs_in_output(target_path):
    out = _run_file_capture_stdout(target_path).strip()
    assert out != "None", f"expected={'not None'!r} actual={out!r}"


def test_pairs_not_modified_nums_length_mismatch(target_path, nums_from_source):
    mod = _load_module_from_path(target_path)
    assert hasattr(mod, "nums")
    actual_nums = mod.nums
    assert isinstance(actual_nums, list), f"expected={list.__name__!r} actual={type(actual_nums).__name__!r}"
    assert len(actual_nums) == len(nums_from_source), f"expected={len(nums_from_source)!r} actual={len(actual_nums)!r}"