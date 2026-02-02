import importlib.util
import os
import sys
import pytest


def load_module(tmp_path, monkeypatch):
    fname = "15_inventoryTransactions.py"
    src = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(src):
        src = fname

    dst = tmp_path / fname
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    mod_name = "invtx_mod_under_test"
    spec = importlib.util.spec_from_file_location(mod_name, str(dst))
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def test_inventory_updated_and_zero_items_removed(tmp_path, monkeypatch, capsys):
    m = load_module(tmp_path, monkeypatch)

    assert isinstance(m.inventory, dict)
    assert m.inventory == {"apple": 2, "orange": 4}

    out = capsys.readouterr().out.strip()
    assert out
    printed = eval(out, {"__builtins__": {}}, {})
    assert printed == m.inventory


def test_no_zero_quantities_remain(tmp_path, monkeypatch):
    m = load_module(tmp_path, monkeypatch)
    assert all(qty != 0 for qty in m.inventory.values())


def test_transactions_list_is_unchanged(tmp_path, monkeypatch):
    m = load_module(tmp_path, monkeypatch)
    assert isinstance(m.transactions, list)
    assert m.transactions == [
        {"item": "apple", "delta": 3},
        {"item": "orange", "delta": 1},
        {"item": "banana", "delta": 2},
        {"item": "banana", "delta": -2},
        {"item": "apple", "delta": -2},
    ]


def test_inventory_contains_only_items_expected_after_processing(tmp_path, monkeypatch):
    m = load_module(tmp_path, monkeypatch)
    assert set(m.inventory.keys()) == {"apple", "orange"}