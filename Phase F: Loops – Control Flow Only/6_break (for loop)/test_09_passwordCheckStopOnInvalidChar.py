import importlib
import contextlib
import io
import string

MODULE_NAME = "09_passwordCheckStopOnInvalidChar"


def run_module():
    mod = importlib.import_module(MODULE_NAME)
    importlib.reload(mod)
    return mod


def test_prints_first_invalid_character():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_module()
    out = buf.getvalue().strip()
    expected = "#"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_outputs_single_character_only():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_module()
    out = buf.getvalue().strip()
    expected_len = 1
    assert len(out) == expected_len, f"expected={expected_len!r} actual={len(out)!r}"


def test_output_is_non_alphanumeric():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_module()
    out = buf.getvalue().strip()
    expected = False
    actual = out.isalnum()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_is_printable():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_module()
    out = buf.getvalue().strip()
    expected = True
    actual = len(out) == 1 and out in string.printable and out not in "\r\n\t"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"