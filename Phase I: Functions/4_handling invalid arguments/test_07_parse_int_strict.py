import pytest
import importlib

mod = importlib.import_module("07_parse_int_strict")
parse_int_strict = mod.parse_int_strict


def test_parses_with_whitespace_and_sign():
    expected = -42
    actual = parse_int_strict("  -42 ")
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize(
    "s, expected",
    [
        ("0", 0),
        ("+0", 0),
        ("-0", 0),
        ("007", 7),
        ("   123   ", 123),
        ("+123", 123),
        ("-123", -123),
        ("\t\n  -9  \r", -9),
    ],
)
def test_valid_inputs(s, expected):
    actual = parse_int_strict(s)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize("s", ["", "   ", "+", "-", "++1", "--1", "+-1", "-+1"])
def test_invalid_empty_or_sign_only(s):
    with pytest.raises(ValueError) as ei:
        parse_int_strict(s)
    expected = "invalid integer literal"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize(
    "s",
    [
        "3.14",
        "1e3",
        "12 3",
        "  1  ",
        "1_000",
        "0x10",
        "NaN",
        "inf",
        "  + 1",
        " - 1",
        "1-",
        "1+",
        " +001x",
        "١٢٣",
    ],
)
def test_invalid_non_digit_patterns_raise_value_error(s):
    with pytest.raises(ValueError) as ei:
        parse_int_strict(s)
    expected = "invalid integer literal"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


@pytest.mark.parametrize("val", [10, 10.0, None, True, False, b"123", bytearray(b"123"), ["1"], {"s": "1"}])
def test_non_str_raises_type_error(val):
    with pytest.raises(TypeError) as ei:
        parse_int_strict(val)
    expected = "s must be a str"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


def test_does_not_truncate_or_round():
    with pytest.raises(ValueError) as ei:
        parse_int_strict("  42.0  ")
    expected = "invalid integer literal"
    actual = str(ei.value)
    assert actual == expected, f"expected {expected}, got {actual}"


def test_preserves_large_integer():
    s = "9" * 60
    expected = int(s)
    actual = parse_int_strict(s)
    assert actual == expected, f"expected {expected}, got {actual}"