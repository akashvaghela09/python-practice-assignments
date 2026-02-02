import importlib.util
import os
import sys
import re


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_summary_output(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_unpackFromDictItems.py")
    mod_name = "unpack_from_dict_items_08"
    _load_module(path, mod_name)

    out = capsys.readouterr().out
    lines = [line.rstrip("\n") for line in out.splitlines()]
    assert lines, f"expected non-empty output vs actual={out!r}"
    actual = lines[-1]

    expected = "apple=1.25, banana=0.75, cherry=2.50"
    assert actual == expected, f"expected={expected!r} vs actual={actual!r}"


def test_parts_and_summary_state(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_unpackFromDictItems.py")
    mod_name = "unpack_from_dict_items_08_state"
    module = _load_module(path, mod_name)
    capsys.readouterr()

    assert hasattr(module, "prices"), "expected prices to exist vs actual missing"
    assert hasattr(module, "parts"), "expected parts to exist vs actual missing"
    assert hasattr(module, "summary"), "expected summary to exist vs actual missing"

    assert isinstance(module.prices, dict), f"expected=dict vs actual={type(module.prices)!r}"
    assert isinstance(module.parts, list), f"expected=list vs actual={type(module.parts)!r}"
    assert isinstance(module.summary, str), f"expected=str vs actual={type(module.summary)!r}"

    expected_parts = ["apple=1.25", "banana=0.75", "cherry=2.50"]
    assert module.parts == expected_parts, f"expected={expected_parts!r} vs actual={module.parts!r}"

    expected_summary = "apple=1.25, banana=0.75, cherry=2.50"
    assert module.summary == expected_summary, f"expected={expected_summary!r} vs actual={module.summary!r}"


def test_formatting_two_decimals_and_order(capsys):
    path = os.path.join(os.path.dirname(__file__), "08_unpackFromDictItems.py")
    mod_name = "unpack_from_dict_items_08_format"
    _load_module(path, mod_name)
    out = capsys.readouterr().out
    actual = out.splitlines()[-1].strip()

    tokens = actual.split(", ")
    expected_order = ["apple", "banana", "cherry"]
    actual_order = [t.split("=", 1)[0] if "=" in t else None for t in tokens]
    assert actual_order == expected_order, f"expected={expected_order!r} vs actual={actual_order!r}"

    for t in tokens:
        assert re.fullmatch(r"[a-z]+=\d+\.\d{2}", t), f"expected pattern vs actual={t!r}"