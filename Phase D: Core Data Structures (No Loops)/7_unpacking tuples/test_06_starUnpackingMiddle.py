import importlib
import io
import sys
import ast
import pytest

MODULE_NAME = "06_starUnpackingMiddle"


def load_module_fresh(monkeypatch):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def test_printed_output_matches_expected(monkeypatch):
    _, out = load_module_fresh(monkeypatch)
    lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    expected = ["5", "[10, 15, 20]", "25"]
    assert lines[:3] == expected, f"expected={expected} actual={lines[:3]}"


def test_variables_exist_and_values(monkeypatch):
    mod, _ = load_module_fresh(monkeypatch)
    assert hasattr(mod, "first"), "expected=hasattr actual=missing"
    assert hasattr(mod, "middle"), "expected=hasattr actual=missing"
    assert hasattr(mod, "last"), "expected=hasattr actual=missing"

    expected_first = 5
    expected_middle = [10, 15, 20]
    expected_last = 25

    assert mod.first == expected_first, f"expected={expected_first} actual={mod.first}"
    assert mod.middle == expected_middle, f"expected={expected_middle} actual={mod.middle}"
    assert mod.last == expected_last, f"expected={expected_last} actual={mod.last}"


def test_middle_is_list(monkeypatch):
    mod, _ = load_module_fresh(monkeypatch)
    expected_type = list
    actual_type = type(getattr(mod, "middle", None))
    assert actual_type is expected_type, f"expected={expected_type} actual={actual_type}"


def test_uses_star_unpacking_in_assignment():
    mod = importlib.import_module(MODULE_NAME)
    src = getattr(mod, "__file__", None)
    assert src is not None

    with open(src, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, (ast.Tuple, ast.List)):
                    elts = tgt.elts
                    if any(isinstance(e, ast.Starred) for e in elts):
                        found = True
                        break
        if found:
            break

    expected = True
    actual = found
    assert actual == expected, f"expected={expected} actual={actual}"