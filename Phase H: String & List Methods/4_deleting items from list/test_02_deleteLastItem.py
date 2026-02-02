import importlib.util
import pathlib


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_deletes_last_item_from_nums():
    path = pathlib.Path(__file__).resolve().parent / "02_deleteLastItem.py"
    mod = load_module(path)
    expected = [10, 20, 30]
    actual = getattr(mod, "nums", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_nums_is_list_and_length_is_three():
    path = pathlib.Path(__file__).resolve().parent / "02_deleteLastItem.py"
    mod = load_module(path)
    actual = getattr(mod, "nums", None)
    assert isinstance(actual, list), f"expected={list} actual={type(actual)}"
    expected_len = 3
    actual_len = len(actual)
    assert actual_len == expected_len, f"expected={expected_len} actual={actual_len}"


def test_last_item_is_thirty():
    path = pathlib.Path(__file__).resolve().parent / "02_deleteLastItem.py"
    mod = load_module(path)
    expected = 30
    actual = getattr(mod, "nums", None)[-1]
    assert actual == expected, f"expected={expected} actual={actual}"