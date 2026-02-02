import importlib.util
import io
import os
import re
import contextlib
import pytest

MODULE_FILENAME = "08_equalityAndFloatTolerance.py"


def _load_and_run_module(path):
    spec = importlib.util.spec_from_file_location("student_module_08", path)
    module = importlib.util.module_from_spec(spec)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        spec.loader.exec_module(module)
    return module, stdout.getvalue()


def test_no_placeholder_remaining():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "__________" not in content


def test_outputs_exact_lines():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    _, out = _load_and_run_module(path)
    lines = [line.rstrip("\n\r") for line in out.splitlines() if line.strip() != ""]
    assert lines == ["False", "True"], f"expected {['False', 'True']} vs actual {lines}"


def test_is_close_matches_tolerance_logic():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    module, _ = _load_and_run_module(path)

    assert hasattr(module, "x")
    assert hasattr(module, "tolerance")
    assert hasattr(module, "is_close")

    expected = abs(module.x - 0.3) < module.tolerance
    assert module.is_close == expected, f"expected {expected} vs actual {module.is_close}"


def test_tolerance_is_positive_number():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    module, _ = _load_and_run_module(path)
    assert isinstance(module.tolerance, (int, float))
    assert module.tolerance > 0


def test_is_close_is_boolean():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    module, _ = _load_and_run_module(path)
    assert isinstance(module.is_close, bool)