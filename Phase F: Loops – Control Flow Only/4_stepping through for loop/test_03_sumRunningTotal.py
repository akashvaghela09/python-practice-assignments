import importlib
import io
import contextlib
import pytest


def test_running_total_output():
    mod_name = "03_sumRunningTotal"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    out = buf.getvalue().strip().splitlines()
    expected = ["total: 15"]
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_running_total_single_print():
    mod_name = "03_sumRunningTotal"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue().strip().splitlines()
    expected_len = 1
    actual_len = len(out)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"


def test_running_total_format_exact():
    mod_name = "03_sumRunningTotal"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue()
    expected = "total: 15\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"