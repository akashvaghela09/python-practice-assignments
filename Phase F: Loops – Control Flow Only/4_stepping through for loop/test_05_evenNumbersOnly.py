import importlib
import io
import contextlib
import pytest


def run_module_capture_stdout(module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_even_numbers_only_output_exact(capsys):
    module_name = "05_evenNumbersOnly"
    expected = "2\n4\n6\n8\n10\n"
    try:
        actual = run_module_capture_stdout(module_name)
    except Exception as e:
        pytest.fail(f"expected={expected!r} actual=raised {type(e).__name__}")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_even_numbers_only_no_extra_output(capsys):
    module_name = "05_evenNumbersOnly"
    expected_lines = ["2", "4", "6", "8", "10"]
    try:
        out = run_module_capture_stdout(module_name)
    except Exception as e:
        pytest.fail(f"expected={expected_lines!r} actual=raised {type(e).__name__}")
    actual_lines = [line for line in out.splitlines() if line != ""]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_even_numbers_only_no_odds_present():
    module_name = "05_evenNumbersOnly"
    try:
        out = run_module_capture_stdout(module_name)
    except Exception as e:
        pytest.fail(f"expected={'no odds in output'!r} actual=raised {type(e).__name__}")
    expected = False
    actual = any(line.strip() in {"1", "3", "5", "7", "9"} for line in out.splitlines())
    assert actual == expected, f"expected={expected!r} actual={actual!r}"