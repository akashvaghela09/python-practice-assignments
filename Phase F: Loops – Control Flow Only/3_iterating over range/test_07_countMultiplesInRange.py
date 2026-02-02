import builtins
import importlib
import io
import sys
import types
import pytest


MODULE_NAME = "07_countMultiplesInRange"


def _run_module_with_input(inputs):
    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    old_input = builtins.input
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    builtins.input = fake_input
    try:
        if MODULE_NAME in sys.modules:
            del sys.modules[MODULE_NAME]
        try:
            importlib.import_module(MODULE_NAME)
        except SyntaxError:
            return "SYNTAX_ERROR"
        except Exception:
            return "RUNTIME_ERROR"
        return sys.stdout.getvalue().strip()
    finally:
        builtins.input = old_input
        sys.stdout = old_stdout


def _expected(a, b, m):
    if m == 0:
        raise ZeroDivisionError
    if a > b:
        return 0
    return sum(1 for n in range(a, b + 1) if n % m == 0)


def test_module_compiles_and_runs_minimal():
    out = _run_module_with_input(["1", "1", "1"])
    assert out not in ("SYNTAX_ERROR", "RUNTIME_ERROR"), f"expected runnable, actual={out}"


@pytest.mark.parametrize(
    "a,b,m",
    [
        (3, 10, 2),
        (1, 10, 3),
        (0, 0, 5),
        (-10, 10, 5),
        (-10, -1, 3),
        (5, 5, 2),
        (5, 5, 5),
        (1, 1, -1),
        (-7, 7, -3),
        (100, 200, 7),
        (-100, 100, 8),
        (9, 2, 3),  # a > b
    ],
)
def test_counts_multiples_various_ranges(a, b, m):
    expected = _expected(a, b, m)
    out = _run_module_with_input([str(a), str(b), str(m)])
    assert out not in ("SYNTAX_ERROR", "RUNTIME_ERROR"), f"expected={expected} actual={out}"
    try:
        actual = int(out)
    except Exception:
        assert False, f"expected={expected} actual={out}"
    assert actual == expected, f"expected={expected} actual={actual}"


def test_m_equals_zero_is_handled_or_errors_cleanly():
    a, b, m = 1, 10, 0
    out = _run_module_with_input([str(a), str(b), str(m)])
    assert out in ("RUNTIME_ERROR", "SYNTAX_ERROR") or out.lstrip("-").isdigit(), f"expected={'RUNTIME_ERROR'} actual={out}"


def test_output_is_single_integer_line():
    a, b, m = -5, 5, 2
    expected = _expected(a, b, m)
    out = _run_module_with_input([str(a), str(b), str(m)])
    assert out not in ("SYNTAX_ERROR", "RUNTIME_ERROR"), f"expected={expected} actual={out}"
    assert "\n" not in out, f"expected={expected} actual={out}"
    assert out.strip() == out, f"expected={expected} actual={out}"
    try:
        actual = int(out)
    except Exception:
        assert False, f"expected={expected} actual={out}"
    assert actual == expected, f"expected={expected} actual={actual}"