import importlib
import sys
import types
import pytest

MODULE_NAME = "01_countUpBasics"


def _run_module_capture_stdout(monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        captured.append(s)

    monkeypatch.setattr("builtins.print", fake_print)

    sys.modules.pop(MODULE_NAME, None)
    try:
        importlib.import_module(MODULE_NAME)
    except Exception as e:
        pytest.fail(f"expected=successful_run actual={type(e).__name__}: {e}")

    out = "".join(captured)
    if out.endswith("\n"):
        out = out[:-1]
    return out


def test_countup_prints_exact_lines(monkeypatch):
    out = _run_module_capture_stdout(monkeypatch)
    expected = "\n".join(str(i) for i in range(1, 6))
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_countup_prints_five_lines(monkeypatch):
    out = _run_module_capture_stdout(monkeypatch)
    lines = [] if out == "" else out.split("\n")
    expected_count = 5
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_countup_lines_are_increasing_by_one(monkeypatch):
    out = _run_module_capture_stdout(monkeypatch)
    lines = [] if out == "" else out.split("\n")
    try:
        nums = [int(x) for x in lines]
    except Exception as e:
        pytest.fail(f"expected=all_int_lines actual={type(e).__name__}: {e}")

    expected = list(range(1, 6))
    assert nums == expected, f"expected={expected!r} actual={nums!r}"


def test_module_defines_no_required_symbols():
    # Ensure import doesn't require specific names; just execution.
    sys.modules.pop(MODULE_NAME, None)
    try:
        mod = importlib.import_module(MODULE_NAME)
    except Exception as e:
        pytest.fail(f"expected=successful_import actual={type(e).__name__}: {e}")

    assert isinstance(mod, types.ModuleType), f"expected={types.ModuleType!r} actual={type(mod)!r}"