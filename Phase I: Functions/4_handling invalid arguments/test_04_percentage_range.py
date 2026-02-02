import pytest
import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent / "04_percentage_range.py"
spec = importlib.util.spec_from_file_location("percentage_range_04", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

clamp_percentage = mod.clamp_percentage


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0.0),
        (100, 100.0),
        (75, 75.0),
        (0.5, 0.5),
        (99.9, 99.9),
    ],
)
def test_valid_values_return_float(value, expected):
    actual = clamp_percentage(value)
    assert type(actual) is float
    assert actual == expected


@pytest.mark.parametrize("value", [-1, -0.0001, 100.0001, 101])
def test_out_of_range_raises_value_error_with_exact_message(value):
    with pytest.raises(ValueError) as exc:
        clamp_percentage(value)
    assert str(exc.value) == "p must be between 0 and 100"


@pytest.mark.parametrize(
    "value",
    [
        "50",
        None,
        object(),
        [],
        {},
        (),
        complex(1, 0),
    ],
)
def test_invalid_type_raises_type_error_with_exact_message(value):
    with pytest.raises(TypeError) as exc:
        clamp_percentage(value)
    assert str(exc.value) == "p must be a number"


@pytest.mark.parametrize("value", [True, False])
def test_bool_is_not_allowed(value):
    with pytest.raises(TypeError) as exc:
        clamp_percentage(value)
    assert str(exc.value) == "p must be a number"


def test_boundary_values_are_accepted():
    assert clamp_percentage(0) == 0.0
    assert clamp_percentage(100) == 100.0