import pytest
import importlib.util
from pathlib import Path

# --- dynamic import for numbered module ---
MODULE_PATH = Path(__file__).parent / "02_non_empty_string.py"

spec = importlib.util.spec_from_file_location("non_empty_string_02", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

require_non_empty_string = module.require_non_empty_string
# -----------------------------------------


@pytest.mark.parametrize(
    "value",
    [None, 123, 12.5, True, False, [], {}, (), object(), b"hi", bytearray(b"hi")],
)
def test_type_error_for_non_str(value):
    with pytest.raises(TypeError) as excinfo:
        require_non_empty_string(value)
    assert str(excinfo.value) == "s must be a str", (
        f"expected {'s must be a str'} vs actual {str(excinfo.value)}"
    )


@pytest.mark.parametrize("value", ["", " ", "   ", "\t", "\n", "\r\n", " \t \n "])
def test_value_error_for_empty_or_whitespace(value):
    with pytest.raises(ValueError) as excinfo:
        require_non_empty_string(value)
    assert str(excinfo.value) == "s must be a non-empty string", (
        f"expected {'s must be a non-empty string'} vs actual {str(excinfo.value)}"
    )


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("hi", "hi"),
        ("  hi", "hi"),
        ("hi  ", "hi"),
        ("  hi  ", "hi"),
        ("\thi\t", "hi"),
        ("\nhi\n", "hi"),
        ("  h i  ", "h i"),
        ("  a\tb  ", "a\tb"),
    ],
)
def test_returns_stripped_string(raw, expected):
    actual = require_non_empty_string(raw)
    assert actual == expected, f"expected {expected!r} vs actual {actual!r}"


def test_returns_new_value_when_stripping_needed():
    raw = "  hi  "
    actual = require_non_empty_string(raw)
    assert actual == "hi", f"expected {'hi'!r} vs actual {actual!r}"
    assert actual is not raw, f"expected {False} vs actual {actual is raw}"


def test_returns_same_object_when_no_stripping_needed():
    raw = "hi"
    actual = require_non_empty_string(raw)
    assert actual == "hi", f"expected {'hi'!r} vs actual {actual!r}"
    assert actual is raw, f"expected {True} vs actual {actual is raw}"
