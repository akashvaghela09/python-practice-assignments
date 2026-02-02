import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILENAME = "06_runningTotal.py"


def _load_module_from_path(path):
    name = "runningTotal_mod_under_test"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(path)
    return buf.getvalue()


def _parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        node = ast.parse(last, mode="eval")
        val = ast.literal_eval(node)
        return val
    except Exception:
        return None


def _expected_running_totals(nums):
    total = 0
    res = []
    for n in nums:
        total += n
        res.append(total)
    return res


def test_script_executes_without_placeholder_syntax(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    try:
        out = _run_script_capture_stdout(str(dst))
    except SyntaxError as e:
        pytest.fail(f"expected=no_syntax_error actual=SyntaxError:{e.msg}")
    except Exception as e:
        pytest.fail(f"expected=no_runtime_error actual={type(e).__name__}")

    assert isinstance(out, str)


def test_prints_correct_running_totals(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    try:
        out = _run_script_capture_stdout(str(dst))
    except Exception as e:
        pytest.fail(f"expected=successful_execution actual={type(e).__name__}")

    parsed = _parse_last_list_from_stdout(out)
    if parsed is None:
        pytest.fail("expected=list_output actual=unparseable_or_missing")

    expected = _expected_running_totals([2, 5, 3, 10])
    assert parsed == expected, f"expected={expected!r} actual={parsed!r}"


def test_running_totals_change_when_input_changes(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    text = open(src, "r", encoding="utf-8").read()

    altered = text.replace("nums = [2, 5, 3, 10]", "nums = [1, 1, 1, 1, 2]")
    if altered == text:
        pytest.skip("could_not_modify_input_list")

    dst = tmp_path / MODULE_FILENAME
    dst.write_text(altered, encoding="utf-8")

    try:
        out = _run_script_capture_stdout(str(dst))
    except Exception as e:
        pytest.fail(f"expected=successful_execution actual={type(e).__name__}")

    parsed = _parse_last_list_from_stdout(out)
    if parsed is None:
        pytest.fail("expected=list_output actual=unparseable_or_missing")

    expected = _expected_running_totals([1, 1, 1, 1, 2])
    assert parsed == expected, f"expected={expected!r} actual={parsed!r}"


def test_running_list_length_matches_input_length_when_modified(tmp_path):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    text = open(src, "r", encoding="utf-8").read()

    altered = text.replace("nums = [2, 5, 3, 10]", "nums = [3, -1, 4]")
    if altered == text:
        pytest.skip("could_not_modify_input_list")

    dst = tmp_path / MODULE_FILENAME
    dst.write_text(altered, encoding="utf-8")

    try:
        out = _run_script_capture_stdout(str(dst))
    except Exception as e:
        pytest.fail(f"expected=successful_execution actual={type(e).__name__}")

    parsed = _parse_last_list_from_stdout(out)
    if parsed is None:
        pytest.fail("expected=list_output actual=unparseable_or_missing")

    expected_len = 3
    actual_len = len(parsed) if isinstance(parsed, list) else None
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"


def test_importing_original_module_does_not_crash():
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    try:
        _run_script_capture_stdout(src)
    except SyntaxError as e:
        pytest.fail(f"expected=no_syntax_error actual=SyntaxError:{e.msg}")
    except Exception as e:
        pytest.fail(f"expected=no_runtime_error actual={type(e).__name__}")