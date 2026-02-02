import importlib.util
import os
import sys
import types
import pytest


def _load_module():
    filename = os.path.join(os.path.dirname(__file__), "03_tupleUnpacking.py")
    module_name = "03_tupleUnpacking"
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_print_output(capsys):
    expected = "255,128,64"
    _load_module()
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_unpacked_values_exist_and_match_expected(capsys):
    expected_r, expected_g, expected_b = 255, 128, 64
    mod = _load_module()
    assert hasattr(mod, "r"), f"expected={'r'!r} actual={dir(mod)!r}"
    assert hasattr(mod, "g"), f"expected={'g'!r} actual={dir(mod)!r}"
    assert hasattr(mod, "b"), f"expected={'b'!r} actual={dir(mod)!r}"
    assert mod.r == expected_r, f"expected={expected_r!r} actual={mod.r!r}"
    assert mod.g == expected_g, f"expected={expected_g!r} actual={mod.g!r}"
    assert mod.b == expected_b, f"expected={expected_b!r} actual={mod.b!r}"


def test_rgb_tuple_intact():
    expected = (255, 128, 64)
    mod = _load_module()
    assert hasattr(mod, "rgb"), f"expected={'rgb'!r} actual={dir(mod)!r}"
    assert isinstance(mod.rgb, tuple), f"expected={tuple!r} actual={type(mod.rgb)!r}"
    assert mod.rgb == expected, f"expected={expected!r} actual={mod.rgb!r}"


def test_unpacked_matches_rgb_tuple():
    mod = _load_module()
    actual = (mod.r, mod.g, mod.b)
    assert actual == mod.rgb, f"expected={mod.rgb!r} actual={actual!r}"