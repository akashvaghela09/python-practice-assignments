import importlib
import math
import pytest

mod = importlib.import_module("08_sum_n_numbers")
sum_n = mod.sum_n


def test_sum_n_basic_examples():
    expected = 3
    actual = sum_n([1, 2, 3, 4], 2)
    assert actual == expected, f"expected {expected}, got {actual}"


def test_sum_n_zero_n():
    expected = 0
    actual = sum_n([10, 20, 30], 0)
    assert actual == expected, f"expected {expected}, got {actual}"


def test_sum_n_full_length():
    nums = [1, 2, 3.5, 4]
    expected = sum(nums)
    actual = sum_n(nums, len(nums))
    assert actual == expected, f"expected {expected}, got {actual}"


def test_sum_n_floats_precision():
    nums = [0.1, 0.2, 0.3]
    expected = sum(nums[:2])
    actual = sum_n(nums, 2)
    assert math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-12), f"expected {expected}, got {actual}"


def test_numbers_must_be_list_typeerror():
    with pytest.raises(TypeError) as ei:
        sum_n((1, 2, 3), 2)
    expected = "numbers must be a list of numbers"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize(
    "bad_numbers",
    [
        [1, "2", 3],
        [1, None, 3],
        [1, object(), 3],
        [True, 2, 3],
        [1, False, 3],
    ],
)
def test_numbers_elements_must_be_int_or_float_bool_not_allowed(bad_numbers):
    with pytest.raises(TypeError) as ei:
        sum_n(bad_numbers, 2)
    expected = "numbers must be a list of numbers"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize("bad_n", [2.0, "2", None, True, False])
def test_n_must_be_int_bool_not_allowed(bad_n):
    with pytest.raises(TypeError) as ei:
        sum_n([1, 2, 3], bad_n)
    expected = "n must be an int"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize("n", [-1, 4, 10])
def test_n_out_of_range_raises_valueerror(n):
    with pytest.raises(ValueError) as ei:
        sum_n([1, 2, 3], n)
    expected = "n out of allowed range"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


def test_empty_list_allows_n_zero_only():
    expected = 0
    actual = sum_n([], 0)
    assert actual == expected, f"expected {expected}, got {actual}"

    with pytest.raises(ValueError) as ei:
        sum_n([], 1)
    expected_msg = "n out of allowed range"
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected {expected_msg}, got {actual_msg}"


def test_does_not_modify_input_list():
    nums = [1, 2, 3, 4]
    before = nums.copy()
    _ = sum_n(nums, 3)
    assert nums == before, f"expected {before}, got {nums}"