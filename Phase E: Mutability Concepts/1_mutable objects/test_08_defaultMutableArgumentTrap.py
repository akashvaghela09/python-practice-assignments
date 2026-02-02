import importlib
import pytest

mod = importlib.import_module("08_defaultMutableArgumentTrap")


def test_add_item_returns_fresh_list_each_time_without_bucket():
    r1 = mod.add_item("a")
    r2 = mod.add_item("b")

    assert isinstance(r1, list), f"expected={list} actual={type(r1)}"
    assert isinstance(r2, list), f"expected={list} actual={type(r2)}"
    assert r1 == ["a"], f"expected={['a']} actual={r1}"
    assert r2 == ["b"], f"expected={['b']} actual={r2}"
    assert r1 is not r2, f"expected={False} actual={r1 is r2}"


def test_add_item_uses_provided_bucket_and_mutates_it():
    bucket = ["x"]
    res = mod.add_item("y", bucket)

    assert res is bucket, f"expected={True} actual={res is bucket}"
    assert bucket == ["x", "y"], f"expected={['x','y']} actual={bucket}"


def test_main_prints_expected_output(capsys, monkeypatch):
    monkeypatch.setattr(mod, "add_item", getattr(mod, "add_item"))
    mod.main()
    out = capsys.readouterr().out
    assert out == "['a']\n['b']\n", f"expected={\"['a']\\n['b']\\n\"} actual={out!r}"