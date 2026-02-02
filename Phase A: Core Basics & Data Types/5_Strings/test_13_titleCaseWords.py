import importlib
import io
import contextlib


def run_module_capture(module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_output_title_case():
    out = run_module_capture("13_titleCaseWords")
    actual = out.strip()
    expected = "The Quick Brown Fox"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_extra_output_lines():
    out = run_module_capture("13_titleCaseWords")
    lines = out.splitlines()
    actual = [ln for ln in lines if ln.strip() != ""]
    expected = ["The Quick Brown Fox"]
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_titled_variable_exists_and_correct():
    mod = importlib.import_module("13_titleCaseWords")
    assert hasattr(mod, "titled")
    actual = getattr(mod, "titled")
    expected = "The Quick Brown Fox"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sentence_unchanged():
    mod = importlib.import_module("13_titleCaseWords")
    assert hasattr(mod, "sentence")
    actual = getattr(mod, "sentence")
    expected = "the quick brown fox"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"