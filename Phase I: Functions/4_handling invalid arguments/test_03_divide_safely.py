import math
import pytest

from 03_divide_safely import divide


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5.0),
        (9, 2, 4.5),
        (-10, 2, -5.0),
        (10.0, 4, 2.5),
        (1, 4, 0.25),
    ],
)
def test_divide_valid_values(a, b, expected):
    actual = divide(a, b)
    assert actual == expected, f"expected {expected} got {actual}"


def test_divide_returns_float_for_int_inputs():
    actual = divide(1, 2)
    assert isinstance(actual, float), f"expected {float.__name__} got {type(actual).__name__}"


def test_divide_by_zero_raises_valueerror_with_message():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    expected_msg = "b must not be zero"
    actual_msg = str(excinfo.value)
    assert actual_msg == expected_msg, f"expected {expected_msg!r} got {actual_msg!r}"


@pytest.mark.parametrize(
    "a,b",
    [
        (True, 2),
        (False, 2),
        (2, True),
        (2, False),
        (True, False),
    ],
)
def test_divide_rejects_bool_inputs(a, b):
    with pytest.raises(TypeError) as excinfo:
        divide(a, b)
    expected_msg = "a and b must be numbers"
    actual_msg = str(excinfo.value)
    assert actual_msg == expected_msg, f"expected {expected_msg!r} got {actual_msg!r}"


@pytest.mark.parametrize(
    "a,b",
    [
        ("10", 2),
        (10, "2"),
        (None, 2),
        (10, None),
        ([], 2),
        (10, []),
        ({}, 2),
        (10, {}),
        (object(), 2),
        (10, object()),
    ],
)
def test_divide_rejects_non_number_inputs(a, b):
    with pytest.raises(TypeError) as excinfo:
        divide(a, b)
    expected_msg = "a and b must be numbers"
    actual_msg = str(excinfo.value)
    assert actual_msg == expected_msg, f"expected {expected_msg!r} got {actual_msg!r}"


def test_divide_zero_numerator_ok():
    actual = divide(0, 5)
    expected = 0.0
    assert actual == expected, f"expected {expected} got {actual}"


def test_divide_negative_zero_denominator_raises():
    with pytest.raises(ValueError) as excinfo:
        divide(10, -0.0)
    expected_msg = "b must not be zero"
    actual_msg = str(excinfo.value)
    assert actual_msg == expected_msg, f"expected {expected_msg!r} got {actual_msg!r}"


def test_divide_float_zero_denominator_raises():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0.0)
    expected_msg = "b must not be zero"
    actual_msg = str(excinfo.value)
    assert actual_msg == expected_msg, f"expected {expected_msg!r} got {actual_msg!r}"


def test_divide_handles_infinite_results():
    actual = divide(1.0, 1e-300)
    assert math.isfinite(actual), f"expected {True} got {math.isfinite(actual)}"