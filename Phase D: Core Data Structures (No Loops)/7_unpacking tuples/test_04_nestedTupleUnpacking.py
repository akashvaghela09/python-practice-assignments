import importlib
import sys
import pytest


MODULE_NAME = "04_nestedTupleUnpacking"


def _import_fresh():
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    return importlib.import_module(MODULE_NAME)


def test_prints_city_and_zip_in_order(capsys):
    _import_fresh()
    out = capsys.readouterr().out.splitlines()
    expected = ["Austin", "78701"]
    actual = [line.strip() for line in out if line.strip() != ""]
    assert actual[:2] == expected, f"expected={expected} actual={actual[:2]}"


def test_exposes_city_and_zip_code_variables():
    m = _import_fresh()
    assert hasattr(m, "city"), f"expected={True} actual={hasattr(m, 'city')}"
    assert hasattr(m, "zip_code"), f"expected={True} actual={hasattr(m, 'zip_code')}"
    assert m.city == "Austin", f"expected={'Austin'} actual={m.city}"
    assert m.zip_code == 78701, f"expected={78701} actual={m.zip_code}"


def test_city_is_str_and_zip_is_int():
    m = _import_fresh()
    assert isinstance(m.city, str), f"expected={str} actual={type(m.city)}"
    assert isinstance(m.zip_code, int), f"expected={int} actual={type(m.zip_code)}"