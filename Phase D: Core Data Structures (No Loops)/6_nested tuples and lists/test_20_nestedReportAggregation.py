import ast
import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout


def _load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_module_20", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec = importlib.util.spec_from_file_location("student_script_20", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return buf.getvalue()


def _parse_last_printed_list_of_tuples(stdout_text):
    lines = [ln.strip() for ln in stdout_text.splitlines() if ln.strip()]
    if not lines:
        raise AssertionError("No output captured")
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception as e:
        raise AssertionError(f"Could not parse printed value: {e}")
    return val


def test_report_prints_expected_aggregation():
    filename = "20_nestedReportAggregation.py"
    out = _run_script_capture_stdout(filename)
    actual = _parse_last_printed_list_of_tuples(out)

    stores = [("A", [5, 7, 7]), ("B", [10, 12]), ("C", [])]
    expected = [(sid, sum(days)) for sid, days in stores]

    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_report_variable_is_list_of_tuples_and_order_preserved():
    filename = "20_nestedReportAggregation.py"
    mod = _load_module_from_filename(filename)

    assert hasattr(mod, "report"), "expected=report_exists actual=missing"
    report = mod.report
    assert isinstance(report, list), f"expected={list.__name__} actual={type(report).__name__}"

    stores = getattr(mod, "stores", None)
    assert isinstance(stores, list), f"expected={list.__name__} actual={type(stores).__name__}"
    assert len(report) == len(stores), f"expected={len(stores)!r} actual={len(report)!r}"

    expected_store_order = [sid for sid, _ in stores]
    actual_store_order = [t[0] for t in report]
    assert actual_store_order == expected_store_order, f"expected={expected_store_order!r} actual={actual_store_order!r}"

    for idx, item in enumerate(report):
        assert isinstance(item, tuple), f"expected=tuple actual={type(item).__name__}"
        assert len(item) == 2, f"expected=2 actual={len(item)!r}"
        sid, total = item
        assert isinstance(sid, str), f"expected=str actual={type(sid).__name__}"
        assert isinstance(total, int), f"expected=int actual={type(total).__name__}"
        expected_total = sum(stores[idx][1])
        assert total == expected_total, f"expected={expected_total!r} actual={total!r}"


def test_no_none_in_report_totals():
    filename = "20_nestedReportAggregation.py"
    mod = _load_module_from_filename(filename)
    report = mod.report
    totals = [t[1] for t in report]
    assert all(x is not None for x in totals), f"expected={True!r} actual={any(x is None for x in totals)!r}"


def test_stdout_contains_single_report_line():
    filename = "20_nestedReportAggregation.py"
    out = _run_script_capture_stdout(filename)
    lines = [ln for ln in out.splitlines() if ln.strip()]
    actual_count = len(lines)
    expected_count = 1
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"

    # ensure it looks like a list of tuples
    last = lines[-1].strip()
    looks_like = bool(re.match(r"^\s*\[.*\]\s*$", last))
    assert looks_like is True, f"expected={True!r} actual={looks_like!r}"