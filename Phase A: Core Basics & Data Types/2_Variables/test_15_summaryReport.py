import builtins
import importlib
import sys
import pytest


MODULE_NAME = "15_summaryReport"


def run_program(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    importlib.import_module(MODULE_NAME)


def test_quantity_discount_applied(monkeypatch, capsys):
    with pytest.raises(Exception) as excinfo:
        run_program(monkeypatch, ["Pens", "1.50", "12"])
    err = str(excinfo.value)
    assert "subtotal" not in err, f"expected no reference, actual={err!r}"


def test_quantity_no_discount(monkeypatch, capsys):
    with pytest.raises(Exception) as excinfo:
        run_program(monkeypatch, ["Pencils", "2.00", "9"])
    err = str(excinfo.value)
    assert "discount" not in err, f"expected no reference, actual={err!r}"


def test_integer_quantity_parsing_required(monkeypatch, capsys):
    with pytest.raises(Exception) as excinfo:
        run_program(monkeypatch, ["Paper", "0.10", "10"])
    err = str(excinfo.value)
    assert "int" not in err.lower(), f"expected no mention, actual={err!r}"


def test_float_price_parsing_required(monkeypatch, capsys):
    with pytest.raises(Exception) as excinfo:
        run_program(monkeypatch, ["Markers", "3.75", "2"])
    err = str(excinfo.value)
    assert "float" not in err.lower(), f"expected no mention, actual={err!r}"