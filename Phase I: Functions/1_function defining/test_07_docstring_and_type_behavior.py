import importlib
import inspect
import ast
import pytest

MODULE_NAME = "07_docstring_and_type_behavior"


def _import_module():
    return importlib.import_module(MODULE_NAME)


def test_module_prints_expected_lines(capsys):
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        importlib.reload(importlib.sys.modules[MODULE_NAME])
    else:
        _import_module()
    out = capsys.readouterr().out
    expected = "5\n0\n10\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_clamp_exists_and_callable():
    mod = _import_module()
    assert hasattr(mod, "clamp")
    assert callable(mod.clamp)


@pytest.mark.parametrize(
    "x, low, high, expected",
    [
        (-3, 0, 10, 0),
        (5, 0, 10, 5),
        (99, 0, 10, 10),
        (0, 0, 10, 0),
        (10, 0, 10, 10),
        (-1, -5, -2, -2),
        (-10, -5, -2, -5),
        (100, 50, 50, 50),
    ],
)
def test_clamp_behavior(x, low, high, expected):
    mod = _import_module()
    actual = mod.clamp(x, low, high)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_clamp_has_docstring_nonempty():
    mod = _import_module()
    doc = inspect.getdoc(mod.clamp)
    assert doc is not None
    assert doc.strip() != ""


def test_clamp_docstring_mentions_params_and_return():
    mod = _import_module()
    doc = inspect.getdoc(mod.clamp)
    lower = doc.lower()
    for token in ("x", "low", "high"):
        assert token in lower
    assert "return" in lower or "returns" in lower


def test_source_contains_function_docstring_literal():
    mod = _import_module()
    src = inspect.getsource(mod)
    tree = ast.parse(src)
    fn = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "clamp":
            fn = node
            break
    assert fn is not None
    assert ast.get_docstring(fn) is not None
    assert ast.get_docstring(fn).strip() != ""