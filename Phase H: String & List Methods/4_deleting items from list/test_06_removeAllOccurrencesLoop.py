import importlib.util
import io
import os
import re
import sys


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(file_path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        _load_module("student_mod_run", file_path)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def _extract_nums_from_output(output):
    m = re.search(r"nums:\s*(\[[^\]]*\])", output)
    if not m:
        return None
    try:
        return eval(m.group(1), {"__builtins__": {}})
    except Exception:
        return None


def test_output_nums_list_matches_expected():
    file_path = os.path.join(os.path.dirname(__file__), "06_removeAllOccurrencesLoop.py")
    out = _run_script_capture_stdout(file_path)
    nums = _extract_nums_from_output(out)
    expected = [1, 2, 3, 4]
    assert nums == expected, f"expected={expected} actual={nums}"


def test_no_zeros_in_final_nums():
    file_path = os.path.join(os.path.dirname(__file__), "06_removeAllOccurrencesLoop.py")
    out = _run_script_capture_stdout(file_path)
    nums = _extract_nums_from_output(out)
    expected = False
    actual = (0 in nums) if isinstance(nums, list) else None
    assert actual == expected, f"expected={expected} actual={actual}"


def test_source_uses_while_loop_and_remove_not_list_comp():
    file_path = os.path.join(os.path.dirname(__file__), "06_removeAllOccurrencesLoop.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    expected_while = True
    actual_while = bool(re.search(r"^\s*while\b", src, flags=re.M))
    assert actual_while == expected_while, f"expected={expected_while} actual={actual_while}"

    expected_remove = True
    actual_remove = ".remove(" in src
    assert actual_remove == expected_remove, f"expected={expected_remove} actual={actual_remove}"

    expected_no_listcomp = False
    actual_listcomp = bool(re.search(r"\[[^\]]*for\s+.+\s+in\s+.+\]", src, flags=re.S))
    assert actual_listcomp == expected_no_listcomp, f"expected={expected_no_listcomp} actual={actual_listcomp}"


def test_source_does_not_use_filtered_rebuild_patterns():
    file_path = os.path.join(os.path.dirname(__file__), "06_removeAllOccurrencesLoop.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    expected = False
    actual = any(p in src for p in ["filter(", "list(filter", "copy()", "nums = [", "nums=[", "nums = list("])
    assert actual == expected, f"expected={expected} actual={actual}"