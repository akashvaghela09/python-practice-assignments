import pytest
import importlib

mod = importlib.import_module("11_open_mode_validator")
validate_open_args = mod.validate_open_args


def test_valid_returns_tuple():
    result = validate_open_args("notes.txt", "r")
    assert isinstance(result, tuple)
    assert result == ("notes.txt", "r")


@pytest.mark.parametrize("path", [None, 123, 0.0, [], {}, (), object()])
def test_path_type_errors_non_str(path):
    with pytest.raises(TypeError) as excinfo:
        validate_open_args(path, "w")
    assert str(excinfo.value) == "path must be a non-empty string"


@pytest.mark.parametrize("path", ["", "   "])
def test_path_empty_or_whitespace_errors(path):
    with pytest.raises(TypeError) as excinfo:
        validate_open_args(path, "w")
    assert str(excinfo.value) == "path must be a non-empty string"


@pytest.mark.parametrize("mode", [None, "", "R", "rw", "x", 1, True, [], {}])
def test_invalid_mode_raises_value_error(mode):
    with pytest.raises(ValueError) as excinfo:
        validate_open_args("notes.txt", mode)
    assert str(excinfo.value) == "invalid mode"


@pytest.mark.parametrize("path", ["notes.md", "notes", "notes.txt.bak", "TXT", "notes.TXT"])
def test_read_mode_requires_txt_extension(path):
    with pytest.raises(ValueError) as excinfo:
        validate_open_args(path, "r")
    assert str(excinfo.value) == "read mode requires .txt file"


@pytest.mark.parametrize("mode", ["w", "a"])
def test_write_append_allow_non_txt(mode):
    result = validate_open_args("notes.md", mode)
    assert result == ("notes.md", mode)


def test_returns_new_tuple_not_same_object():
    path = "notes.txt"
    mode = "r"
    result = validate_open_args(path, mode)
    assert result is not (path, mode)
    assert result[0] == path
    assert result[1] == mode