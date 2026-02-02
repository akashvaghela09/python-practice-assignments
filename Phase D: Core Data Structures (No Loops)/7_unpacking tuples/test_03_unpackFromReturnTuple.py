import importlib
import sys
import pytest


def load_module_with_print_capture(monkeypatch, module_name):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)

    if module_name in sys.modules:
        del sys.modules[module_name]
    mod = importlib.import_module(module_name)
    return mod, "".join(captured)


def test_import_prints_expected_and_defines_lo_hi(monkeypatch):
    mod, out = load_module_with_print_capture(monkeypatch, "03_unpackFromReturnTuple")
    actual = out.strip()
    expected = "2 9"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert hasattr(mod, "lo")
    assert hasattr(mod, "hi")
    assert mod.lo == 2, f"expected={2!r} actual={mod.lo!r}"
    assert mod.hi == 9, f"expected={9!r} actual={mod.hi!r}"


def test_stats_returns_min_max():
    mod = importlib.import_module("03_unpackFromReturnTuple")
    assert mod.stats([7, 2, 9, 4]) == (2, 9), f"expected={(2,9)!r} actual={mod.stats([7,2,9,4])!r}"
    assert mod.stats([-1, -5, 0]) == (-5, 0), f"expected={(-5,0)!r} actual={mod.stats([-1,-5,0])!r}"


def test_lo_hi_match_stats_values(monkeypatch):
    mod, _ = load_module_with_print_capture(monkeypatch, "03_unpackFromReturnTuple")
    expected = mod.stats(mod.values)
    actual = (mod.lo, mod.hi)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"