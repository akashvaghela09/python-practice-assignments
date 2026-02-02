import builtins
import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "05_listFromUserInputSplit.py"


def _load_module_with_input(monkeypatch, input_value):
    monkeypatch.setattr(builtins, "input", lambda _: input_value)
    mod_name = f"student_{os.path.splitext(MODULE_FILENAME)[0]}"
    spec = importlib.util.spec_from_file_location(mod_name, MODULE_FILENAME)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return module, buf.getvalue()


def test_creates_colors_list_and_prints(monkeypatch):
    module, out = _load_module_with_input(monkeypatch, "red, blue, green")
    assert hasattr(module, "colors")
    assert isinstance(module.colors, list)
    assert module.colors == ["red", "blue", "green"], f"expected {['red','blue','green']} got {module.colors}"
    printed = out.strip()
    assert printed != ""
    assert printed == str(module.colors), f"expected {str(module.colors)} got {printed}"


def test_strips_whitespace_around_items(monkeypatch):
    module, out = _load_module_with_input(monkeypatch, "  red ,blue  ,  green ")
    assert module.colors == ["red", "blue", "green"], f"expected {['red','blue','green']} got {module.colors}"
    assert out.strip() == str(module.colors), f"expected {str(module.colors)} got {out.strip()}"


def test_preserves_case_and_inner_spaces(monkeypatch):
    module, out = _load_module_with_input(monkeypatch, "Light Blue,Deep  Red, Green ")
    expected = ["Light Blue", "Deep  Red", "Green"]
    assert module.colors == expected, f"expected {expected} got {module.colors}"
    assert out.strip() == str(module.colors), f"expected {str(module.colors)} got {out.strip()}"


def test_exactly_three_values(monkeypatch):
    module, _ = _load_module_with_input(monkeypatch, "a,b,c")
    assert len(module.colors) == 3, f"expected {3} got {len(module.colors)}"