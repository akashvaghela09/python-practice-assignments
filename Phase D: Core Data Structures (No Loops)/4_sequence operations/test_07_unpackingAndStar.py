import importlib
import ast
import pathlib
import sys
import pytest

EXPECTED_FIRST = "red"
EXPECTED_MIDDLE = ["green", "blue"]
EXPECTED_LAST = "yellow"


def _load_module():
    if "07_unpackingAndStar" in sys.modules:
        del sys.modules["07_unpackingAndStar"]
    return importlib.import_module("07_unpackingAndStar")


def test_unpacking_values(capsys):
    mod = _load_module()
    assert getattr(mod, "first", None) == EXPECTED_FIRST
    assert getattr(mod, "middle", None) == EXPECTED_MIDDLE
    assert getattr(mod, "last", None) == EXPECTED_LAST

    out = capsys.readouterr().out.strip().splitlines()
    assert out == [EXPECTED_FIRST, str(EXPECTED_MIDDLE), EXPECTED_LAST]


def test_unpacking_uses_starred_target():
    source = pathlib.Path("07_unpackingAndStar.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    assert assigns, "Expected vs actual: at least one assignment, found none"

    def has_starred_unpack(a: ast.Assign) -> bool:
        for t in a.targets:
            if isinstance(t, ast.Tuple):
                return any(isinstance(elt, ast.Starred) for elt in t.elts)
        return False

    assert any(has_starred_unpack(a) for a in assigns), "Expected vs actual: starred unpacking present, not found"


def test_unpacking_assigned_from_colors_name():
    source = pathlib.Path("07_unpackingAndStar.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    found = False
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Tuple) and any(isinstance(e, ast.Starred) for e in t.elts):
                    if isinstance(node.value, ast.Name) and node.value.id == "colors":
                        found = True
    assert found, "Expected vs actual: assignment from 'colors', not found"