import importlib.util
import io
import os
import sys


def _load_module():
    filename = "05_iterateKeysValues.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("iterateKeysValues_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_inventory_exists_and_is_dict():
    mod = _load_module()
    assert hasattr(mod, "inventory")
    assert isinstance(mod.inventory, dict)


def test_prints_expected_inventory_lines_in_order():
    captured = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = captured
        mod = _load_module()
    finally:
        sys.stdout = old

    expected_lines = [f"{k}={v}" for k, v in mod.inventory.items()]
    actual_lines = [line.rstrip("\n") for line in captured.getvalue().splitlines() if line.strip() != ""]

    assert expected_lines == actual_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_prints_one_line_per_item_no_extra_nonempty_lines():
    captured = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = captured
        mod = _load_module()
    finally:
        sys.stdout = old

    nonempty_lines = [line for line in captured.getvalue().splitlines() if line.strip() != ""]
    expected_count = len(mod.inventory)

    assert expected_count == len(nonempty_lines), f"expected={expected_count!r} actual={len(nonempty_lines)!r}"