import pytest
import importlib

mod = importlib.import_module("06_repeat_string")
repeat = mod.repeat


@pytest.mark.parametrize(
    "s,times,expected",
    [
        ("ab", 3, "ababab"),
        ("", 5, ""),
        ("x", 0, ""),
        ("🙂", 4, "🙂🙂🙂🙂"),
        ("ab", 1, "ab"),
    ],
)
def test_repeat_valid_cases(s, times, expected):
    actual = repeat(s, times)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


@pytest.mark.parametrize(
    "s",
    [None, 1, 1.5, [], {}, (), object()],
)
def test_repeat_s_type_errors(s):
    with pytest.raises(TypeError) as ei:
        repeat(s, 1)
    assert str(ei.value) == "s must be a str", f"expected={'s must be a str'!r} actual={str(ei.value)!r}"


@pytest.mark.parametrize(
    "times",
    [None, 1.0, "3", [], {}, (), object(), True, False],
)
def test_repeat_times_type_errors(times):
    with pytest.raises(TypeError) as ei:
        repeat("a", times)
    assert str(ei.value) == "times must be an int", f"expected={'times must be an int'!r} actual={str(ei.value)!r}"


@pytest.mark.parametrize("times", [-1, -2, -100])
def test_repeat_times_value_errors(times):
    with pytest.raises(ValueError) as ei:
        repeat("a", times)
    assert str(ei.value) == "times must be non-negative", f"expected={'times must be non-negative'!r} actual={str(ei.value)!r}"


def test_repeat_returns_new_string_value_not_required_identity():
    s = "ab"
    out = repeat(s, 2)
    assert out == "abab", f"expected={'abab'!r} actual={out!r}"