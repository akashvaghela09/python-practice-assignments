import importlib.util
import pathlib
import sys
import types
import pytest


FILE_NAME = "05_multipleReturns_absolute.py"


def _load_module(tmp_path):
    src = pathlib.Path(__file__).with_name(FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, importlib.abc.Loader)
    spec.loader.exec_module(mod)
    return mod


def test_absolute_value_exists_and_callable(tmp_path):
    mod = _load_module(tmp_path)
    assert hasattr(mod, "absolute_value")
    assert callable(mod.absolute_value)


@pytest.mark.parametrize(
    "n",
    [-1, -2, -9, -123, 0, 1, 2, 9, 123],
)
def test_absolute_value_correct_for_various_values(tmp_path, n):
    mod = _load_module(tmp_path)
    expected = abs(n)
    actual = mod.absolute_value(n)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_absolute_value_returns_int_for_int_input(tmp_path):
    mod = _load_module(tmp_path)
    out = mod.absolute_value(-7)
    assert isinstance(out, int)


def test_printed_output_matches_expected(tmp_path, capsys):
    _load_module(tmp_path)
    captured = capsys.readouterr()
    expected = "8\n5\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"