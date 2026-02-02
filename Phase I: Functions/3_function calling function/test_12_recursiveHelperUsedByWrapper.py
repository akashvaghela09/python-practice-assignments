import ast
import importlib.util
import pathlib
import sys
import types
import pytest

MODULE_NAME = "12_recursiveHelperUsedByWrapper"


def _load_module_without_executing_print():
    path = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    new_body = []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Call):
            call = node.value
            if isinstance(call.func, ast.Name) and call.func.id == "print":
                continue
        new_body.append(node)
    tree.body = new_body
    ast.fix_missing_locations(tree)

    mod = types.ModuleType(MODULE_NAME)
    mod.__file__ = str(path)
    sys.modules[MODULE_NAME] = mod
    code = compile(tree, str(path), "exec")
    exec(code, mod.__dict__)
    return mod, source


@pytest.fixture(scope="module")
def mod_and_source():
    return _load_module_without_executing_print()


def test_digit_sum_calls_helper(mod_and_source, monkeypatch):
    mod, _ = mod_and_source
    if not hasattr(mod, "digit_sum") or not hasattr(mod, "digit_sum_helper"):
        pytest.fail("missing required functions")

    called = {"count": 0, "arg": None}

    def fake_helper(n):
        called["count"] += 1
        called["arg"] = n
        return 12345

    monkeypatch.setattr(mod, "digit_sum_helper", fake_helper, raising=True)
    out = mod.digit_sum(999)

    assert called["count"] == 1
    assert called["arg"] == 999
    assert out == 12345


def test_digit_sum_helper_is_recursive_no_loops(mod_and_source):
    _, source = mod_and_source
    tree = ast.parse(source)

    helper_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "digit_sum_helper":
            helper_node = node
            break
    assert helper_node is not None

    has_loop = any(isinstance(n, (ast.For, ast.While, ast.AsyncFor)) for n in ast.walk(helper_node))
    assert has_loop is False

    recursive_calls = 0
    for n in ast.walk(helper_node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "digit_sum_helper":
            recursive_calls += 1
    assert recursive_calls >= 1


def test_digit_sum_4096_prints_19(capsys):
    importlib.invalidate_caches()
    path = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    spec = importlib.util.spec_from_file_location(f"{MODULE_NAME}_run", str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    captured = capsys.readouterr()
    assert captured.out == "19\n"