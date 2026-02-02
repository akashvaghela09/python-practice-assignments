import pytest
import importlib

mod = importlib.import_module("12_normalize_slice")
normalize_slice = mod.normalize_slice


def _assert_raises_with_message(exc_type, msg, func, *args, **kwargs):
    with pytest.raises(exc_type) as ei:
        func(*args, **kwargs)
    assert str(ei.value) == msg, f"expected={msg!r} actual={str(ei.value)!r}"


@pytest.mark.parametrize("seq_len", [-1, -10])
def test_seq_len_negative_raises_valueerror(seq_len):
    _assert_raises_with_message(
        ValueError,
        "seq_len must be a non-negative int",
        normalize_slice,
        seq_len,
    )


@pytest.mark.parametrize("seq_len", [1.0, "10", None, object(), [10], (10,), {10}])
def test_seq_len_non_int_type_raises_valueerror(seq_len):
    _assert_raises_with_message(
        ValueError,
        "seq_len must be a non-negative int",
        normalize_slice,
        seq_len,
    )


def test_seq_len_bool_not_allowed_raises_valueerror():
    _assert_raises_with_message(
        ValueError,
        "seq_len must be a non-negative int",
        normalize_slice,
        True,
    )


@pytest.mark.parametrize("start", [1.0, "1", object(), [1], (1,), {1}, False, True])
def test_start_invalid_type_raises_typeerror(start):
    _assert_raises_with_message(
        TypeError,
        "start/stop must be int or None",
        normalize_slice,
        10,
        start,
        None,
        1,
    )


@pytest.mark.parametrize("stop", [1.0, "1", object(), [1], (1,), {1}, False, True])
def test_stop_invalid_type_raises_typeerror(stop):
    _assert_raises_with_message(
        TypeError,
        "start/stop must be int or None",
        normalize_slice,
        10,
        None,
        stop,
        1,
    )


@pytest.mark.parametrize("step", [0, 0.0, "1", None, object(), False, True])
def test_step_invalid_raises_valueerror(step):
    _assert_raises_with_message(
        ValueError,
        "step must be a non-zero int",
        normalize_slice,
        10,
        None,
        None,
        step,
    )


def test_expected_example_positive_step():
    assert normalize_slice(10, 2, None, 2) == (2, 10, 2)


def test_expected_example_step_zero_raises():
    _assert_raises_with_message(
        ValueError,
        "step must be a non-zero int",
        normalize_slice,
        5,
        0,
        5,
        0,
    )


@pytest.mark.parametrize(
    "seq_len,start,stop,step",
    [
        (0, None, None, 1),
        (1, None, None, 1),
        (10, None, None, 1),
        (10, 0, None, 1),
        (10, None, 0, 1),
        (10, 0, 10, 1),
        (10, -1, None, 1),
        (10, None, -1, 1),
        (10, 100, None, 1),
        (10, None, 100, 1),
        (10, -100, None, 1),
        (10, None, -100, 1),
        (10, 3, 7, 2),
        (10, 7, 3, -1),
        (10, None, None, -1),
        (10, -2, -8, -2),
        (10, 8, None, -2),
        (10, None, 2, -2),
        (5, 4, 0, -1),
        (5, 0, 4, 1),
    ],
)
def test_matches_slice_indices(seq_len, start, stop, step):
    expected = slice(start, stop, step).indices(seq_len)
    actual = normalize_slice(seq_len, start, stop, step)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_defaults_match_slice_indices():
    expected = slice(None, None, 1).indices(10)
    actual = normalize_slice(10)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_start_stop_none_allowed():
    expected = slice(None, None, 2).indices(7)
    actual = normalize_slice(7, None, None, 2)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_step_negative_with_none_bounds_matches_slice():
    expected = slice(None, None, -3).indices(11)
    actual = normalize_slice(11, None, None, -3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"