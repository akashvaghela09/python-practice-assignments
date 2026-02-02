import importlib.util
import io
import contextlib
import os
import sys
import pytest

MODULE_FILE = "06_variablePositionalArgsSum.py"


def load_module(tmp_path):
    spec = importlib.util.spec_from_file_location("student_mod", os.path.abspath(MODULE_FILE))
    mod = importlib.util.module_from_spec(spec)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        spec.loader.exec_module(mod)
    return mod, out.getvalue()


def test_module_prints_expected_output(tmp_path):
    _, printed = load_module(tmp_path)
    expected = "0\n6\n10\n"
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


@pytest.mark.parametrize(
    "args, expected",
    [
        ((), 0),
        ((1, 2, 3), 6),
        ((10,), 10),
        ((-1, 1, 5), 5),
        ((0, 0, 0), 0),
        ((1.5, 2.5), 4.0),
    ],
)
def test_total_returns_sum(args, expected, tmp_path):
    mod, _ = load_module(tmp_path)
    actual = mod.total(*args)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_total_accepts_many_args(tmp_path):
    mod, _ = load_module(tmp_path)
    args = tuple(range(100))
    expected = sum(args)
    actual = mod.total(*args)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_total_function_exists(tmp_path):
    mod, _ = load_module(tmp_path)
    assert hasattr(mod, "total")
    assert callable(mod.total)