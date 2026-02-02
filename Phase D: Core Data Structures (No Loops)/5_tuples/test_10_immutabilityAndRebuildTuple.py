import importlib.util
import pathlib
import sys

import pytest


def load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_updated_tuple_value_and_original_unchanged(capsys):
    path = pathlib.Path(__file__).resolve().parent / "10_immutabilityAndRebuildTuple.py"
    module_name = "student_10_immutabilityAndRebuildTuple"
    mod = load_module_from_path(module_name, path)

    captured = capsys.readouterr()
    out = captured.out.strip()
    expected_out = "(1, 99, 3, 4)"
    assert out == expected_out, f"expected={expected_out!r} actual={out!r}"

    expected_updated = (1, 99, 3, 4)
    actual_updated = getattr(mod, "updated", None)
    assert actual_updated == expected_updated, f"expected={expected_updated!r} actual={actual_updated!r}"

    expected_original = (1, 2, 3, 4)
    actual_original = getattr(mod, "original", None)
    assert actual_original == expected_original, f"expected={expected_original!r} actual={actual_original!r}"

    assert isinstance(actual_updated, tuple), f"expected={tuple!r} actual={type(actual_updated)!r}"
    assert isinstance(actual_original, tuple), f"expected={tuple!r} actual={type(actual_original)!r}"


def test_updated_is_new_object_not_original():
    path = pathlib.Path(__file__).resolve().parent / "10_immutabilityAndRebuildTuple.py"
    module_name = "student_10_immutabilityAndRebuildTuple_obj"
    mod = load_module_from_path(module_name, path)

    original = getattr(mod, "original", None)
    updated = getattr(mod, "updated", None)

    assert updated is not original, f"expected={False!r} actual={(updated is original)!r}"