import importlib
import contextlib
import io
import inspect
import ast
import textwrap
import pytest

MODULE_NAME = "04_helperForMath"


def load_module_with_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def test_import_prints_expected_output():
    mod, out = load_module_with_stdout()
    expected = "25\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_square_basic_values():
    mod, _ = load_module_with_stdout()
    cases = [0, 1, 2, -3, 10, -11]
    for n in cases:
        expected = n * n
        actual = mod.square(n)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sum_of_squares_basic_values():
    mod, _ = load_module_with_stdout()
    cases = [(0, 0), (1, 2), (3, 4), (-3, 4), (-5, -6), (10, -11)]
    for a, b in cases:
        expected = a * a + b * b
        actual = mod.sum_of_squares(a, b)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_sum_of_squares_uses_square_function_call():
    mod, _ = load_module_with_stdout()
    src = textwrap.dedent(inspect.getsource(mod.sum_of_squares))
    tree = ast.parse(src)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    name_calls = []
    for c in calls:
        if isinstance(c.func, ast.Name):
            name_calls.append(c.func.id)
        elif isinstance(c.func, ast.Attribute):
            name_calls.append(c.func.attr)
    assert "square" in name_calls, f"expected={'square'!r} actual={name_calls!r}"


def test_sum_of_squares_calls_square_twice_for_ints(monkeypatch):
    mod, _ = load_module_with_stdout()
    call_args = []

    def spy(n):
        call_args.append(n)
        return n * n

    monkeypatch.setattr(mod, "square", spy)
    a, b = 7, -8
    expected = a * a + b * b
    actual = mod.sum_of_squares(a, b)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    expected_calls = [a, b]
    assert call_args == expected_calls, f"expected={expected_calls!r} actual={call_args!r}"