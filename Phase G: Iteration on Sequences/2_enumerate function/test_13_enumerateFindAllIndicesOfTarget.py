import importlib.util
import pathlib
import sys
import ast
import pytest


FILE_NAME = "13_enumerateFindAllIndicesOfTarget.py"


def load_module_from_path(path):
    module_name = "mod_13_enumerateFindAllIndicesOfTarget"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def get_expected_indices():
    data = ["x", "y", "x", "y", "y", "z"]
    target = "y"
    return [i for i, v in enumerate(data) if v == target]


def test_script_runs_and_indices_correct(tmp_path, capsys):
    src_path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    code = src_path.read_text(encoding="utf-8")
    test_file = tmp_path / FILE_NAME
    test_file.write_text(code, encoding="utf-8")

    mod = load_module_from_path(test_file)
    expected = get_expected_indices()

    assert hasattr(mod, "indices")
    assert mod.indices == expected, f"expected={expected} actual={getattr(mod, 'indices', None)}"

    out = capsys.readouterr().out.strip()
    assert out, f"expected={str(expected)} actual={out}"
    assert out.endswith(str(expected)), f"expected={str(expected)} actual={out}"


def test_uses_enumerate_in_for_loop():
    src_path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    code = src_path.read_text(encoding="utf-8")
    tree = ast.parse(code)

    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert for_nodes, "expected=for-loop actual=none"

    found = False
    for n in for_nodes:
        call = n.iter
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "enumerate":
            found = True
            break
    assert found, "expected=enumerate actual=not_found"


def test_indices_are_appended(tmp_path):
    src_path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    code = src_path.read_text(encoding="utf-8")
    test_file = tmp_path / FILE_NAME
    test_file.write_text(code, encoding="utf-8")

    mod = load_module_from_path(test_file)

    assert isinstance(mod.indices, list)
    assert all(isinstance(i, int) for i in mod.indices), f"expected=all_int actual={mod.indices}"