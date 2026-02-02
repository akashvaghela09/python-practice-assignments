import importlib.util
import os
import sys
import types
import pytest


@pytest.fixture(scope="module")
def mod():
    filename = "10_returningMultipleValuesToCaller.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("m10_returningMultipleValuesToCaller", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_print_output_exact(capsys):
    filename = "10_returningMultipleValuesToCaller.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("m10_returningMultipleValuesToCaller_print", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    expected = "8\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_min_max_exists_and_callable(mod):
    assert hasattr(mod, "min_max"), "expected=True actual=False"
    assert callable(mod.min_max), "expected=callable actual=not_callable"


def test_range_width_exists_and_callable(mod):
    assert hasattr(mod, "range_width"), "expected=True actual=False"
    assert callable(mod.range_width), "expected=callable actual=not_callable"


def test_min_max_returns_tuple_of_two(mod):
    nums = [10, 2, 8, 3]
    res = mod.min_max(nums)
    assert isinstance(res, tuple), f"expected={tuple!r} actual={type(res)!r}"
    assert len(res) == 2, f"expected=2 actual={len(res)!r}"


def test_min_max_correctness_various(mod):
    cases = [
        [10, 2, 8, 3],
        [5, 5, 5],
        [-1, -3, -2, -4],
        [0, 100, -100, 50],
        [7, 1],
    ]
    for nums in cases:
        expected = (min(nums), max(nums))
        actual = mod.min_max(list(nums))
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_range_width_correctness_various(mod):
    cases = [
        [10, 2, 8, 3],
        [5, 5, 5],
        [-1, -3, -2, -4],
        [0, 100, -100, 50],
        [7, 1],
    ]
    for nums in cases:
        expected = max(nums) - min(nums)
        actual = mod.range_width(list(nums))
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_range_width_uses_min_max(monkeypatch, mod):
    calls = {"n": 0}

    def wrapped(nums):
        calls["n"] += 1
        return (min(nums), max(nums))

    monkeypatch.setattr(mod, "min_max", wrapped, raising=True)
    res = mod.range_width([3, 9, 1])
    expected = 9 - 1
    assert calls["n"] == 1, f"expected=1 actual={calls['n']!r}"
    assert res == expected, f"expected={expected!r} actual={res!r}"


def test_inputs_not_modified(mod):
    nums = [3, 1, 2]
    original = list(nums)
    _ = mod.min_max(nums)
    assert nums == original, f"expected={original!r} actual={nums!r}"
    nums2 = [10, -1, 4, 4]
    original2 = list(nums2)
    _ = mod.range_width(nums2)
    assert nums2 == original2, f"expected={original2!r} actual={nums2!r}"