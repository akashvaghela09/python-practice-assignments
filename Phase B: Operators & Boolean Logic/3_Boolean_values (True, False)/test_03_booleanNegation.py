import importlib
import io
import contextlib
import sys
import types
import pathlib
import pytest


MODULE_NAME = "03_booleanNegation"


def _import_fresh():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _import_fresh()
    return mod, buf.getvalue()


def test_module_imports_without_syntax_error():
    _import_fresh()


def test_is_raining_exists_and_is_bool():
    mod = _import_fresh()
    assert hasattr(mod, "is_raining")
    assert isinstance(mod.is_raining, bool)


def test_is_dry_exists_and_is_bool():
    mod = _import_fresh()
    assert hasattr(mod, "is_dry")
    assert isinstance(mod.is_dry, bool)


def test_is_dry_is_negation_of_is_raining():
    mod = _import_fresh()
    expected = (not mod.is_raining)
    actual = mod.is_dry
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_output_two_lines_boolean_values():
    mod, out = _run_module_capture_stdout()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    expected = [str(mod.is_raining), str(mod.is_dry)]
    actual = lines
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_is_dry_is_not_same_object_as_is_raining_when_possible():
    mod = _import_fresh()
    expected = mod.is_dry is (not mod.is_raining)
    actual = True
    assert actual == expected, f"expected={expected!r} actual={actual!r}"