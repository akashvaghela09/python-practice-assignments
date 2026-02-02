import importlib
import ast
import contextlib
import io
import re
import pytest


def load_module():
    return importlib.import_module("15_deepImmutabilityAudit")


def parse_printed_value(line, label):
    prefix = f"{label}:"
    assert line.startswith(prefix)
    return line[len(prefix):].strip()


def safe_literal_eval(value_str):
    try:
        return ast.literal_eval(value_str)
    except Exception:
        return None


def test_script_prints_expected_headers_and_formats(capsys):
    load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 3
    assert out[0].startswith("type:")
    assert out[1].startswith("hashable:")
    assert out[2].startswith("frozen_repr:")


def test_freeze_returns_deeply_immutable_and_hashable():
    mod = load_module()

    frozen = mod.freeze(mod.data)
    assert isinstance(frozen, tuple)

    try:
        h = hash(frozen)
    except Exception as e:
        pytest.fail(f"expected: hashable True, actual: {type(e).__name__}")
    assert isinstance(h, int)

    frozen_dict = dict(frozen)
    assert set(frozen_dict.keys()) == set(mod.data.keys())
    assert isinstance(frozen_dict["a"], tuple)
    assert frozen_dict["a"] == (1, 2)
    assert isinstance(frozen_dict["b"], frozenset)
    assert frozen_dict["b"] == frozenset({3, 4})
    assert isinstance(frozen_dict["c"], tuple)
    assert dict(frozen_dict["c"]) == {"x": 9}


def test_freeze_does_not_mutate_original_input():
    mod = load_module()
    original = {
        "b": {3, 4},
        "a": [1, 2],
        "c": {"x": 9},
    }
    _ = mod.freeze(original)
    assert original == {
        "b": {3, 4},
        "a": [1, 2],
        "c": {"x": 9},
    }
    assert isinstance(original["a"], list)
    assert isinstance(original["b"], set)
    assert isinstance(original["c"], dict)


def test_dict_freeze_sorted_key_order():
    mod = load_module()
    obj = {"b": 1, "a": 2, "c": 3}
    frozen = mod.freeze(obj)
    assert isinstance(frozen, tuple)
    keys_in_order = [k for k, _ in frozen]
    assert keys_in_order == sorted(obj.keys())


def test_script_outputs_type_hashable_and_repr_consistent_with_freeze(capsys):
    mod = load_module()
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 3

    printed_type = parse_printed_value(out[0], "type")
    printed_hashable = parse_printed_value(out[1], "hashable")
    printed_repr = parse_printed_value(out[2], "frozen_repr")

    frozen = mod.freeze(mod.data)
    expected_type = type(frozen).__name__

    assert printed_type == expected_type

    try:
        hash(frozen)
        expected_hashable = "True"
    except Exception:
        expected_hashable = "False"

    assert printed_hashable == expected_hashable

    printed_value = safe_literal_eval(printed_repr)
    assert printed_value is not None, f"expected: literal_eval success, actual: {printed_repr}"

    expected_value = safe_literal_eval(repr(frozen))
    assert expected_value is not None, f"expected: literal_eval success, actual: {repr(frozen)}"

    assert printed_value == expected_value


def test_freeze_nested_structures_and_primitives():
    mod = load_module()
    obj = {
        "z": [{"k": {1, 2}}, 3, None, True, 1.5, "s"],
        "a": {"inner": [1, {"x": 2}]},
    }
    frozen = mod.freeze(obj)
    assert isinstance(frozen, tuple)
    d = dict(frozen)
    assert isinstance(d["z"], tuple)
    assert isinstance(d["z"][0], tuple)
    assert dict(d["z"][0])["k"] == frozenset({1, 2})
    assert d["z"][1:] == (3, None, True, 1.5, "s")
    assert isinstance(d["a"], tuple)
    a_inner = dict(d["a"])["inner"]
    assert isinstance(a_inner, tuple)
    assert a_inner[0] == 1
    assert isinstance(a_inner[1], tuple)
    assert dict(a_inner[1]) == {"x": 2}