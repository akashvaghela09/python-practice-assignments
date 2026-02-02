import importlib
import io
import contextlib
import re


def test_printed_output_exact():
    mod_name = "07_operatorPrecedence"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    out = buf.getvalue()
    expected = "Result: 16\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_result_value_is_16():
    mod = importlib.import_module("07_operatorPrecedence")
    expected = 16
    actual = getattr(mod, "result", object())
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_result_is_int():
    mod = importlib.import_module("07_operatorPrecedence")
    actual = getattr(mod, "result", None)
    expected = int
    assert type(actual) is expected, f"expected={expected!r} actual={type(actual)!r}"


def test_no_extra_output_whitespace_lines():
    mod_name = "07_operatorPrecedence"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue()
    expected_lines = ["Result: 16"]
    actual_lines = [line for line in out.splitlines()]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_output_format_matches():
    mod_name = "07_operatorPrecedence"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue()
    expected = True
    actual = bool(re.fullmatch(r"Result:\s16\n", out))
    assert actual == expected, f"expected={expected!r} actual={actual!r}"