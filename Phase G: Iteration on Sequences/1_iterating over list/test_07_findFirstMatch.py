import importlib.util
import os
import sys


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    try:
        from io import StringIO

        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(module)
        output = buf.getvalue()
    finally:
        sys.stdout = old_stdout

    return module, output


def test_prints_expected_first_match(capsys):
    path = os.path.join(os.path.dirname(__file__), "07_findFirstMatch.py")
    module, out = _run_module_capture_stdout(path)
    printed = out.strip().splitlines()[-1] if out.strip().splitlines() else ""
    expected = str(getattr(module, "result", ""))
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_result_is_first_number_greater_than_10_and_from_list():
    path = os.path.join(os.path.dirname(__file__), "07_findFirstMatch.py")
    module, _ = _run_module_capture_stdout(path)

    nums = getattr(module, "nums", None)
    result = getattr(module, "result", None)

    expected = None
    for n in nums:
        if n > 10:
            expected = n
            break

    assert result == expected, f"expected={expected!r} actual={result!r}"


def test_result_is_not_none_and_greater_than_10():
    path = os.path.join(os.path.dirname(__file__), "07_findFirstMatch.py")
    module, _ = _run_module_capture_stdout(path)

    result = getattr(module, "result", None)
    expected = True
    actual = result is not None and result > 10
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_result_is_first_match_not_any_later_match():
    path = os.path.join(os.path.dirname(__file__), "07_findFirstMatch.py")
    module, _ = _run_module_capture_stdout(path)

    nums = getattr(module, "nums", None)
    result = getattr(module, "result", None)

    first_index = next((i for i, n in enumerate(nums) if n > 10), None)
    result_index = nums.index(result) if result in nums else None

    assert result_index == first_index, f"expected={first_index!r} actual={result_index!r}"