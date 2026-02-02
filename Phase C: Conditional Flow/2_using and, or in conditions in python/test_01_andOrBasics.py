import importlib.util
import os
import sys
import types
import pytest

FILE_NAME = "01_andOrBasics.py"


def _load_module(path):
    name = os.path.splitext(os.path.basename(path))[0] + "_mod"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exec_with_globals(path, g):
    code = compile(open(path, "r", encoding="utf-8").read(), path, "exec")
    exec(code, g, g)


@pytest.mark.parametrize(
    "number, low, high, expected",
    [
        (7, 5, 10, "IN RANGE"),
        (3, 5, 10, "OUT OF RANGE"),
    ],
)
def test_range_check_prints_expected(capsys, number, low, high, expected):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    g = {"__name__": "__main__", "number": number, "low": low, "high": high}
    _exec_with_globals(path, g)
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_default_values_print_in_range(capsys):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    _load_module(path)
    out = capsys.readouterr().out.strip()
    assert out == "IN RANGE", f"expected={'IN RANGE'!r} actual={out!r}"


@pytest.mark.parametrize(
    "number, low, high, expected",
    [
        (5, 5, 10, "IN RANGE"),
        (10, 5, 10, "IN RANGE"),
        (4, 5, 10, "OUT OF RANGE"),
        (11, 5, 10, "OUT OF RANGE"),
        (7, 7, 7, "IN RANGE"),
        (6, 7, 7, "OUT OF RANGE"),
    ],
)
def test_edge_cases_inclusive_range(capsys, number, low, high, expected):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    g = {"__name__": "__main__", "number": number, "low": low, "high": high}
    _exec_with_globals(path, g)
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected!r} actual={out!r}"