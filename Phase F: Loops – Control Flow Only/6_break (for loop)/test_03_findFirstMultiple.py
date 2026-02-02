import importlib.util
import io
import os
import sys


def _run_module(path):
    spec = importlib.util.spec_from_file_location("target_module", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return buf.getvalue(), module


def test_prints_first_multiple_of_7_and_stops():
    path = os.path.join(os.path.dirname(__file__), "03_findFirstMultiple.py")
    out, _ = _run_module(path)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    expected_lines = ["21"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"


def test_no_extra_whitespace_or_additional_output_lines():
    path = os.path.join(os.path.dirname(__file__), "03_findFirstMultiple.py")
    out, _ = _run_module(path)
    lines_raw = out.splitlines()
    nonempty = [ln for ln in lines_raw if ln.strip() != ""]
    expected_count = 1
    actual_count = len(nonempty)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_logic_is_general_first_divisible_by_7():
    path = os.path.join(os.path.dirname(__file__), "03_findFirstMultiple.py")
    _, module = _run_module(path)

    nums = getattr(module, "nums", None)
    assert isinstance(nums, list), f"expected={list!r} actual={type(nums)!r}"

    expected = None
    for n in nums:
        if n % 7 == 0:
            expected = n
            break

    out, _ = _run_module(path)
    printed = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    actual = int(printed[0]) if printed and printed[0].lstrip("-").isdigit() else None
    assert actual == expected, f"expected={expected!r} actual={actual!r}"