import builtins
import importlib.util
import io
import os
import sys
import pytest

MODULE_FILE = "01_breakOnSentinel.py"


def load_module_with_io(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        spec = importlib.util.spec_from_file_location("student_mod", os.path.join(os.getcwd(), MODULE_FILE))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout

    return buf.getvalue()


def test_counts_until_sentinel(monkeypatch):
    out = load_module_with_io(monkeypatch, ["3", "8", "-1"])
    expected = "You entered 2 numbers\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_immediate_sentinel(monkeypatch):
    out = load_module_with_io(monkeypatch, ["-1"])
    expected = "You entered 0 numbers\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_counts_multiple(monkeypatch):
    out = load_module_with_io(monkeypatch, ["10", "0", "7", "-1"])
    expected = "You entered 3 numbers\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"