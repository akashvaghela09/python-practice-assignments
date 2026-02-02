import importlib
import io
import contextlib
import re

MODULE_NAME = "09_ternary_nested_grade_band"

def run_module_capture_stdout():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return buf.getvalue()

def test_prints_expected_single_letter_grade():
    out = run_module_capture_stdout()
    actual = out.strip()
    expected = "B"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

def test_output_has_no_extra_characters_or_lines():
    out = run_module_capture_stdout()
    expected = "B\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"

def test_grade_variable_is_string_and_correct():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    actual = getattr(mod, "grade", None)
    expected = "B"
    assert isinstance(actual, str), f"expected={str!r} actual={type(actual)!r}"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

def test_score_value_int_and_expected():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    actual = getattr(mod, "score", None)
    expected = 84
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert isinstance(actual, int), f"expected={int!r} actual={type(actual)!r}"

def test_grade_only_valid_letter():
    out = run_module_capture_stdout()
    actual = out.strip()
    assert re.fullmatch(r"[ABC]", actual) is not None, f"expected={'[ABC]'!r} actual={actual!r}"