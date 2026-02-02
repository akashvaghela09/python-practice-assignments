import ast
import importlib.util
import pathlib


def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sorted_keys_value_and_order(capsys):
    path = pathlib.Path(__file__).with_name("11_sortByValue.py")
    mod = load_module_from_path(path)

    expected = sorted(mod.scores, key=mod.scores.get, reverse=True)
    assert mod.sorted_keys == expected, f"expected={expected} actual={mod.sorted_keys}"

    out = capsys.readouterr().out.strip()
    assert out, f"expected={str(expected)} actual={out}"
    try:
        printed = ast.literal_eval(out)
    except Exception:
        assert False, f"expected={str(expected)} actual={out}"
    assert printed == expected, f"expected={expected} actual={printed}"


def test_sorted_keys_is_list():
    path = pathlib.Path(__file__).with_name("11_sortByValue.py")
    mod = load_module_from_path(path)
    assert isinstance(mod.sorted_keys, list), f"expected={list} actual={type(mod.sorted_keys)}"