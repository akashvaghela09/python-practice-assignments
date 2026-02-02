import importlib.util
import pathlib
import sys


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "06_sumValidIntegersFromStrings.py"
    name = "mod_06_sumValidIntegersFromStrings"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_printed_total_is_correct(capsys):
    _load_module()
    out = capsys.readouterr().out.strip()
    assert out == "15", f"expected=15 actual={out}"


def test_total_variable_is_correct(capsys):
    m = _load_module()
    capsys.readouterr()
    assert hasattr(m, "total")
    assert m.total == 15, f"expected=15 actual={m.total}"


def test_items_unchanged_content_order(capsys):
    m = _load_module()
    capsys.readouterr()
    assert hasattr(m, "items")
    expected = ["10", "-3", "x", " 5 ", "7.2", "3"]
    assert m.items == expected, f"expected={expected!r} actual={m.items!r}"


def test_total_is_int_type(capsys):
    m = _load_module()
    capsys.readouterr()
    assert isinstance(m.total, int), f"expected={int} actual={type(m.total)}"