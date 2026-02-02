import importlib
import pytest


def test_list_slice_assignment_result(capfd):
    mod = importlib.import_module("06_listSliceAssignment")
    expected = [0, 1, 99, 100, 4, 5]
    assert hasattr(mod, "nums"), f"expected has nums: True, actual has nums: {hasattr(mod, 'nums')}"
    assert mod.nums == expected, f"expected nums: {expected}, actual nums: {mod.nums}"

    out, err = capfd.readouterr()
    assert err == "", f"expected stderr: {''}, actual stderr: {err}"
    printed = out.strip()
    assert printed == str(expected), f"expected stdout: {str(expected)}, actual stdout: {printed}"


def test_nums_is_list():
    mod = importlib.import_module("06_listSliceAssignment")
    assert isinstance(mod.nums, list), f"expected type: {list}, actual type: {type(mod.nums)}"