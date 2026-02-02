import importlib
import sys
import pytest


MODULE_NAME = "06_keywordArguments_formatName"


def _import_module_fresh(monkeypatch, capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    module = importlib.import_module(MODULE_NAME)
    out = capsys.readouterr().out
    return module, out


def test_printed_output_exact(monkeypatch, capsys):
    _, out = _import_module_fresh(monkeypatch, capsys)
    expected = "Lovelace, Ada\nTuring, Alan Mathison\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_format_name_no_middle(monkeypatch, capsys):
    module, _ = _import_module_fresh(monkeypatch, capsys)
    assert hasattr(module, "format_name"), "expected=True actual=False"
    got = module.format_name(first="Ada", last="Lovelace")
    expected = "Lovelace, Ada"
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_format_name_with_middle(monkeypatch, capsys):
    module, _ = _import_module_fresh(monkeypatch, capsys)
    got = module.format_name(last="Turing", first="Alan", middle="Mathison")
    expected = "Turing, Alan Mathison"
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_format_name_middle_empty_string(monkeypatch, capsys):
    module, _ = _import_module_fresh(monkeypatch, capsys)
    got = module.format_name(first="Alan", last="Turing", middle="")
    expected = "Turing, Alan"
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_format_name_middle_whitespace_is_not_empty(monkeypatch, capsys):
    module, _ = _import_module_fresh(monkeypatch, capsys)
    got = module.format_name(first="Ada", last="Lovelace", middle=" ")
    expected = "Lovelace, Ada  "
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_function_signature_defaults(monkeypatch, capsys):
    module, _ = _import_module_fresh(monkeypatch, capsys)
    import inspect

    sig = inspect.signature(module.format_name)
    params = list(sig.parameters.values())

    assert [p.name for p in params] == ["first", "last", "middle"], f"expected={['first','last','middle']!r} actual={[p.name for p in params]!r}"
    assert params[2].default == "", f"expected={''!r} actual={params[2].default!r}"