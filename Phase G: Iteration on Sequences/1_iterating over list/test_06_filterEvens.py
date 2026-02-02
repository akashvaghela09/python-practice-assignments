import importlib
import io
import ast
import contextlib
import pytest

MODULE_NAME = "06_filterEvens"


def _import_fresh():
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def _run_and_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _import_fresh()
    return buf.getvalue()


def _parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    assert lines, f"expected_output_present=True actual_output_present={bool(lines)}"
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception as e:
        pytest.fail(f"expected_last_line_is_list_literal=True actual_error={type(e).__name__}")
    assert isinstance(val, list), f"expected_type=list actual_type={type(val).__name__}"
    return val


def test_script_runs_without_syntax_or_name_errors():
    try:
        _run_and_capture_stdout()
    except Exception as e:
        pytest.fail(f"expected_no_exception=True actual_exception={type(e).__name__}")


def test_prints_only_even_numbers_list():
    out = _run_and_capture_stdout()
    evens = _parse_last_list_from_stdout(out)
    expected = [2, 4, 6]
    assert evens == expected, f"expected={expected!r} actual={evens!r}"


def test_output_contains_only_integers_and_all_even():
    out = _run_and_capture_stdout()
    evens = _parse_last_list_from_stdout(out)

    types_ok = all(isinstance(x, int) for x in evens)
    assert types_ok, f"expected_all_ints=True actual_all_ints={types_ok}"

    all_even = all(x % 2 == 0 for x in evens)
    assert all_even, f"expected_all_even=True actual_all_even={all_even}"


def test_evens_in_ascending_order_and_unique():
    out = _run_and_capture_stdout()
    evens = _parse_last_list_from_stdout(out)

    is_sorted = evens == sorted(evens)
    assert is_sorted, f"expected_sorted=True actual_sorted={is_sorted}"

    unique = len(evens) == len(set(evens))
    assert unique, f"expected_unique=True actual_unique={unique}"