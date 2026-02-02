import importlib.util
import os
import sys
import pytest


def _load_module():
    fname = "01_indexingAndSlicing.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("assignment_mod_01_indexingAndSlicing", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_import_runs_without_error(capsys):
    try:
        mod = _load_module()
    except Exception as e:
        pytest.fail(f"expected import to succeed; actual={type(e).__name__}: {e}")
    assert mod is not None


@pytest.mark.parametrize(
    "varname, expected",
    [
        ("first_char", "p"),
        ("last_char", "n"),
        ("middle", "ytho"),
    ],
)
def test_extracted_values(varname, expected):
    try:
        mod = _load_module()
    except Exception as e:
        pytest.fail(f"expected import to succeed; actual={type(e).__name__}: {e}")

    if not hasattr(mod, varname):
        pytest.fail(f"expected attribute={varname}; actual=missing")

    actual = getattr(mod, varname)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_output_exact_lines(capsys):
    try:
        _load_module()
    except Exception as e:
        pytest.fail(f"expected import to succeed; actual={type(e).__name__}: {e}")

    out = capsys.readouterr().out.splitlines()
    expected_lines = ["p", "n", "ytho"]
    assert out == expected_lines, f"expected={expected_lines!r} actual={out!r}"


def test_word_unchanged():
    try:
        mod = _load_module()
    except Exception as e:
        pytest.fail(f"expected import to succeed; actual={type(e).__name__}: {e}")

    if not hasattr(mod, "word"):
        pytest.fail("expected attribute=word; actual=missing")

    actual = mod.word
    expected = "python"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"