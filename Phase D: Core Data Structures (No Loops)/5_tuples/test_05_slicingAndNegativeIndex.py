import importlib.util
import os
import sys
import pytest

MODULE_FILENAME = "05_slicingAndNegativeIndex.py"


def load_module(capsys):
    path = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("slicing_negative_index_mod", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def test_printed_output_exact(capsys):
    _, out = load_module(capsys)
    expected = "e\n('b', 'c', 'd')\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_exist_and_types(capsys):
    mod, _ = load_module(capsys)
    assert hasattr(mod, "items"), "expected=True actual=False"
    assert hasattr(mod, "last_item"), "expected=True actual=False"
    assert hasattr(mod, "middle"), "expected=True actual=False"
    assert isinstance(mod.items, tuple), f"expected={tuple} actual={type(mod.items)}"
    assert isinstance(mod.middle, tuple), f"expected={tuple} actual={type(mod.middle)}"


def test_values_match_expected(capsys):
    mod, _ = load_module(capsys)
    expected_last = mod.items[-1]
    expected_middle = mod.items[1:4]
    assert mod.last_item == expected_last, f"expected={expected_last!r} actual={mod.last_item!r}"
    assert mod.middle == expected_middle, f"expected={expected_middle!r} actual={mod.middle!r}"


def test_middle_is_slice_not_single_item(capsys):
    mod, _ = load_module(capsys)
    expected_len = 3
    actual_len = len(mod.middle)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"
    assert all(x in mod.items for x in mod.middle), f"expected={True!r} actual={all(x in mod.items for x in mod.middle)!r}"