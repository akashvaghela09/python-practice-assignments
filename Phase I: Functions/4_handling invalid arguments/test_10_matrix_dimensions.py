import importlib.util
import os
import sys
import pytest

MODULE_NAME = "10_matrix_dimensions"
FILE_NAME = "10_matrix_dimensions.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


mod = _load_module()
validate_matrix = mod.validate_matrix


def test_valid_square_matrix_returns_dims():
    matrix = [[1, 2], [3, 4]]
    expected = (2, 2)
    actual = validate_matrix(matrix)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_valid_rectangular_matrix_returns_dims():
    matrix = [[1.0, 2, 3], [4, 5.5, 6]]
    expected = (2, 3)
    actual = validate_matrix(matrix)
    assert actual == expected, f"expected={expected} actual={actual}"


@pytest.mark.parametrize(
    "matrix",
    [
        None,
        123,
        "not a matrix",
        (),
        {},
        set(),
        [],
    ],
)
def test_invalid_matrix_type_or_empty_raises_typeerror(matrix):
    expected_msg = "matrix must be a non-empty list of non-empty lists"
    with pytest.raises(TypeError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


@pytest.mark.parametrize(
    "matrix",
    [
        [1, 2, 3],
        [[1, 2], "ab"],
        [[1, 2], 3],
        [[1, 2], None],
        [[1, 2], ()],
        [[1, 2], {}],
        [[1, 2], []],
        [[]],
        [[1, 2], []],
    ],
)
def test_invalid_rows_not_non_empty_list_raises_typeerror(matrix):
    expected_msg = "matrix must be a non-empty list of non-empty lists"
    with pytest.raises(TypeError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


def test_rows_different_lengths_raises_valueerror():
    matrix = [[1, 2], [3]]
    expected_msg = "matrix rows must have the same length"
    with pytest.raises(ValueError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


def test_rows_different_lengths_three_rows_raises_valueerror():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8]]
    expected_msg = "matrix rows must have the same length"
    with pytest.raises(ValueError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


@pytest.mark.parametrize(
    "bad_elem",
    [True, False, "1", None, [], {}, (), object()],
)
def test_non_numeric_element_raises_typeerror(bad_elem):
    matrix = [[1, 2], [3, bad_elem]]
    expected_msg = "matrix elements must be numbers"
    with pytest.raises(TypeError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


def test_bool_elements_are_not_allowed_even_though_bool_is_int_subclass():
    matrix = [[1, 2], [3, True]]
    expected_msg = "matrix elements must be numbers"
    with pytest.raises(TypeError) as ei:
        validate_matrix(matrix)
    actual_msg = str(ei.value)
    assert actual_msg == expected_msg, f"expected={expected_msg!r} actual={actual_msg!r}"


def test_mixed_int_float_allowed():
    matrix = [[1, 2.5], [3.0, 4]]
    expected = (2, 2)
    actual = validate_matrix(matrix)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_single_row_matrix_dims():
    matrix = [[7, 8, 9]]
    expected = (1, 3)
    actual = validate_matrix(matrix)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_single_column_matrix_dims():
    matrix = [[1], [2], [3]]
    expected = (3, 1)
    actual = validate_matrix(matrix)
    assert actual == expected, f"expected={expected} actual={actual}"