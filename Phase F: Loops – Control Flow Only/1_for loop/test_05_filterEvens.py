import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILE = "05_filterEvens.py"


def _load_module_from_file(path):
    name = "mod_05_filterEvens"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_file_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_file(path)
    return buf.getvalue()


def _parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def _expected_from_nums(nums):
    return [n for n in nums if isinstance(n, int) and n % 2 == 0]


def test_file_exists():
    assert os.path.exists(MODULE_FILE)


def test_script_runs_without_syntax_error():
    try:
        _run_file_capture_stdout(MODULE_FILE)
    except SyntaxError as e:
        pytest.fail(str(e))


def test_output_is_list_of_evens_matches_nums():
    out = _run_file_capture_stdout(MODULE_FILE)
    printed = _parse_last_list_from_stdout(out)
    assert isinstance(printed, list), f"expected=list actual={type(printed).__name__}"
    mod = _load_module_from_file(MODULE_FILE)
    expected = _expected_from_nums(getattr(mod, "nums", None))
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_evens_variable_matches_expected_and_printed():
    out = _run_file_capture_stdout(MODULE_FILE)
    printed = _parse_last_list_from_stdout(out)
    mod = _load_module_from_file(MODULE_FILE)

    nums = getattr(mod, "nums", None)
    evens = getattr(mod, "evens", None)

    assert isinstance(nums, list), f"expected=list actual={type(nums).__name__}"
    assert isinstance(evens, list), f"expected=list actual={type(evens).__name__}"

    expected = _expected_from_nums(nums)
    assert evens == expected, f"expected={expected!r} actual={evens!r}"
    assert printed == evens, f"expected={evens!r} actual={printed!r}"


def test_evens_are_all_even_and_subset_of_nums():
    mod = _load_module_from_file(MODULE_FILE)
    nums = getattr(mod, "nums", None)
    evens = getattr(mod, "evens", None)

    assert isinstance(nums, list), f"expected=list actual={type(nums).__name__}"
    assert isinstance(evens, list), f"expected=list actual={type(evens).__name__}"

    all_even = all(isinstance(x, int) and x % 2 == 0 for x in evens)
    assert all_even, f"expected=True actual={all_even}"

    from collections import Counter

    cn = Counter(nums)
    ce = Counter(evens)
    is_subset_multiset = all(ce[k] <= cn.get(k, 0) for k in ce)
    assert is_subset_multiset, f"expected=True actual={is_subset_multiset}"