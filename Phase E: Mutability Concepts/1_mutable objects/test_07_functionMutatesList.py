import importlib.util
import pathlib
import sys
import types
import pytest

MODULE_NAME = "07_functionMutatesList"
FILE_NAME = "07_functionMutatesList.py"


def _load_module():
    test_dir = pathlib.Path(__file__).resolve().parent
    path = test_dir / FILE_NAME
    if not path.exists():
        path = pathlib.Path(FILE_NAME).resolve()
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def mod():
    return _load_module()


def test_double_in_place_mutates_same_list_object(mod):
    data = [1, 2, 3]
    original_id = id(data)
    mod.double_in_place(data)
    assert id(data) == original_id, f"expected {original_id} actual {id(data)}"


def test_double_in_place_changes_values_in_place(mod):
    data = [1, 2, 3]
    expected = [2, 4, 6]
    mod.double_in_place(data)
    assert data == expected, f"expected {expected} actual {data}"


def test_double_in_place_works_with_empty_list(mod):
    data = []
    expected = []
    mod.double_in_place(data)
    assert data == expected, f"expected {expected} actual {data}"


def test_double_in_place_works_with_negative_and_zero(mod):
    data = [0, -1, 5]
    expected = [0, -2, 10]
    mod.double_in_place(data)
    assert data == expected, f"expected {expected} actual {data}"


def test_main_prints_expected_output_exactly(mod, capsys):
    mod.main()
    out = capsys.readouterr().out
    expected = "[2, 4, 6]\n"
    assert out == expected, f"expected {expected!r} actual {out!r}"