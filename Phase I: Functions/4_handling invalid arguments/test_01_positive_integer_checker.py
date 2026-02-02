import importlib.util
import pathlib
import pytest

MODULE_FILENAME = "01_positive_integer_checker.py"
MODULE_NAME = "positive_integer_checker_01"


def load_module():
    path = pathlib.Path(__file__).resolve().parent / MODULE_FILENAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def mod():
    return load_module()


@pytest.mark.parametrize("n", [1, 2, 3, 10, 999999])
def test_valid_positive_int_returns_true(mod, n):
    assert mod.validate_positive_int(n) is True


@pytest.mark.parametrize("n", [0, -1, -10])
def test_non_positive_int_raises_value_error_with_message(mod, n):
    with pytest.raises(ValueError) as ei:
        mod.validate_positive_int(n)
    assert str(ei.value) == "n must be positive", f"expected={'n must be positive'} actual={str(ei.value)!r}"


@pytest.mark.parametrize(
    "n",
    [
        "3",
        3.0,
        1.2,
        None,
        [],
        {},
        (),
        object(),
        True,
        False,
    ],
)
def test_non_int_raises_type_error_with_message(mod, n):
    with pytest.raises(TypeError) as ei:
        mod.validate_positive_int(n)
    assert str(ei.value) == "n must be an int", f"expected={'n must be an int'} actual={str(ei.value)!r}"


def test_bool_is_not_accepted_even_though_it_is_int_subclass(mod):
    with pytest.raises(TypeError) as ei:
        mod.validate_positive_int(True)
    assert str(ei.value) == "n must be an int", f"expected={'n must be an int'} actual={str(ei.value)!r}"


def test_value_error_has_priority_over_return_for_zero(mod):
    with pytest.raises(ValueError) as ei:
        mod.validate_positive_int(0)
    assert str(ei.value) == "n must be positive", f"expected={'n must be positive'} actual={str(ei.value)!r}"