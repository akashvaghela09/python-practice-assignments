import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


MODULE_FILENAME = "04_listUpdateAndInsert.py"


def _run_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_04", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _parse_printed_list(stdout_text):
    lines = [ln.strip() for ln in stdout_text.splitlines() if ln.strip()]
    if not lines:
        raise AssertionError(f"expected print output, actual={stdout_text!r}")
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception as e:
        raise AssertionError(f"expected printed Python literal list, actual={last!r}") from e
    return val


def test_colors_final_value_and_print_matches():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    mod, out = _run_module_capture_stdout(path)

    assert hasattr(mod, "colors"), f"expected colors variable to exist, actual={dir(mod)!r}"

    expected = ["red", "blue", "green", "yellow"]
    actual_var = mod.colors
    assert actual_var == expected, f"expected={expected!r} actual={actual_var!r}"

    actual_printed = _parse_printed_list(out)
    assert actual_printed == expected, f"expected={expected!r} actual={actual_printed!r}"


def test_colors_is_list_and_ordering_constraints():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    mod, _ = _run_module_capture_stdout(path)

    assert isinstance(mod.colors, list), f"expected={list!r} actual={type(mod.colors)!r}"

    expected_len = 4
    actual_len = len(mod.colors)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"

    expected_third = "green"
    actual_third = mod.colors[2]
    assert actual_third == expected_third, f"expected={expected_third!r} actual={actual_third!r}"

    expected_last = "yellow"
    actual_last = mod.colors[-1]
    assert actual_last == expected_last, f"expected={expected_last!r} actual={actual_last!r}"


def test_prints_list_once_or_last_line_is_list():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    _, out = _run_module_capture_stdout(path)
    printed = _parse_printed_list(out)
    assert isinstance(printed, list), f"expected={list!r} actual={type(printed)!r}"