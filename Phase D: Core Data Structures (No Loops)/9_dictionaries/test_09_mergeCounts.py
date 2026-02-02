import importlib
import ast
import pytest


def _load_module():
    return importlib.import_module("09_mergeCounts")


def _parse_printed_dict(output: str):
    s = output.strip()
    if not s:
        raise AssertionError("expected non-empty output; actual was empty")
    try:
        obj = ast.literal_eval(s)
    except Exception as e:
        raise AssertionError(f"expected dict-like output; actual was {s!r}") from e
    if not isinstance(obj, dict):
        raise AssertionError(f"expected dict output; actual was {type(obj).__name__}")
    return obj


def test_prints_expected_merged_dict(capsys):
    importlib.invalidate_caches()
    importlib.reload(_load_module())
    out = capsys.readouterr().out
    got = _parse_printed_dict(out)
    expected = {"apple": 5, "banana": 2, "orange": 5}
    assert got == expected, f"expected {expected!r} vs actual {got!r}"


def test_merged_variable_is_correct_dict():
    importlib.invalidate_caches()
    mod = importlib.reload(_load_module())
    expected = {"apple": 5, "banana": 2, "orange": 5}
    assert isinstance(mod.merged, dict), f"expected {'dict'} vs actual {type(mod.merged).__name__}"
    assert mod.merged == expected, f"expected {expected!r} vs actual {mod.merged!r}"


def test_c1_and_c2_not_mutated():
    importlib.invalidate_caches()
    mod = importlib.reload(_load_module())
    expected_c1 = {"apple": 2, "banana": 2, "orange": 1}
    expected_c2 = {"apple": 3, "orange": 4}
    assert mod.c1 == expected_c1, f"expected {expected_c1!r} vs actual {mod.c1!r}"
    assert mod.c2 == expected_c2, f"expected {expected_c2!r} vs actual {mod.c2!r}"


def test_merged_is_not_alias_of_c1_or_c2():
    importlib.invalidate_caches()
    mod = importlib.reload(_load_module())
    assert mod.merged is not mod.c1, f"expected {True!r} vs actual {(mod.merged is mod.c1)!r}"
    assert mod.merged is not mod.c2, f"expected {True!r} vs actual {(mod.merged is mod.c2)!r}"


def test_keys_are_union_of_inputs():
    importlib.invalidate_caches()
    mod = importlib.reload(_load_module())
    expected_keys = set(mod.c1) | set(mod.c2)
    got_keys = set(mod.merged)
    assert got_keys == expected_keys, f"expected {expected_keys!r} vs actual {got_keys!r}"