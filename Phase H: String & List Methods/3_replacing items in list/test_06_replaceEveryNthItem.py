import importlib.util
import os
import ast
import pytest

MODULE_FILENAME = "06_replaceEveryNthItem.py"


def _load_module(path):
    spec = importlib.util.spec_from_file_location("student_mod_06", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_list():
    items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(2, len(items), 3):
        items[i] = 'X'
    return items


@pytest.fixture
def module_path():
    here = os.path.dirname(__file__)
    return os.path.join(here, MODULE_FILENAME)


def test_prints_expected_list(module_path, capsys):
    _load_module(module_path)
    out = capsys.readouterr().out.strip()
    expected = str(_expected_list())
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_items_variable_modified_correctly(module_path, capsys):
    mod = _load_module(module_path)
    expected = _expected_list()
    actual = getattr(mod, "items", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_replaced_positions_only(module_path, capsys):
    mod = _load_module(module_path)
    actual = getattr(mod, "items", None)
    expected = _expected_list()
    assert isinstance(actual, list), f"expected={list!r} actual={type(actual)!r}"

    replaced_idx = [i for i, v in enumerate(expected) if v == 'X']
    expected_replaced_idx = list(range(2, 10, 3))
    assert replaced_idx == expected_replaced_idx, f"expected={expected_replaced_idx!r} actual={replaced_idx!r}"

    non_replaced_idx = [i for i, v in enumerate(expected) if v != 'X']
    for i in non_replaced_idx:
        assert actual[i] != 'X', f"expected={False!r} actual={(actual[i] == 'X')!r}"


def test_uses_range_with_step_three(module_path):
    with open(module_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    range_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "range":
            range_calls.append(node)

    assert range_calls, f"expected={True!r} actual={False!r}"

    found_step_3 = False
    for call in range_calls:
        if len(call.args) == 3:
            step = call.args[2]
            if isinstance(step, ast.Constant) and step.value == 3:
                found_step_3 = True
        elif len(call.args) == 1:
            pass
        elif len(call.args) == 2:
            pass

    assert found_step_3, f"expected={True!r} actual={False!r}"