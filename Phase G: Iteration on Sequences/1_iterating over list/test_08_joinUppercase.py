import importlib
import io
import contextlib
import os
import sys
import pytest

MODULE_NAME = "08_joinUppercase"


def run_module_capture():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if MODULE_NAME in sys.modules:
            del sys.modules[MODULE_NAME]
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def test_prints_expected_output_exact():
    out = run_module_capture()
    expected = "CAT-DOG-FISH\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output_whitespace():
    out = run_module_capture()
    expected = "CAT-DOG-FISH"
    actual = out.rstrip("\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert out.count("\n") == 1, f"expected={1!r} actual={out.count('\n')!r}"


def test_module_executes_without_input(monkeypatch):
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    out = run_module_capture()
    expected = "CAT-DOG-FISH\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_source_has_no_blanks_remaining():
    here = os.path.dirname(__file__)
    path = os.path.join(here, f"{MODULE_NAME}.py")
    if not os.path.exists(path):
        path = f"{MODULE_NAME}.py"
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    expected = 0
    actual = src.count("____")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"