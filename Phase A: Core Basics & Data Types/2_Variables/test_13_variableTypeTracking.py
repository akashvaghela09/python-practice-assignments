import importlib.util
import sys
from pathlib import Path
import pytest


MODULE_FILE = "13_variableTypeTracking.py"


def load_module(monkeypatch, input_value):
    monkeypatch.setattr("builtins.input", lambda: input_value)
    spec = importlib.util.spec_from_file_location("student_mod", Path(MODULE_FILE))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["student_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_script(monkeypatch, capsys, input_value):
    mod = load_module(monkeypatch, input_value)
    out = capsys.readouterr().out.splitlines()
    return mod, out


def test_outputs_three_lines(monkeypatch, capsys):
    _, out = run_script(monkeypatch, capsys, "3.5")
    assert len(out) == 3


def test_outputs_exact_format_for_sample(monkeypatch, capsys):
    _, out = run_script(monkeypatch, capsys, "3.5")
    assert out[0] == "text=3.5"
    assert out[1] == "as_float=3.5"
    assert out[2] == "as_int=3"


def test_type_tracking_and_values(monkeypatch, capsys):
    mod, out = run_script(monkeypatch, capsys, "42.9")
    assert hasattr(mod, "text")
    assert hasattr(mod, "as_float")
    assert hasattr(mod, "as_int")
    assert isinstance(mod.text, str)
    assert isinstance(mod.as_float, float)
    assert isinstance(mod.as_int, int)

    expected_text = "text=42.9"
    expected_as_float = f"as_float={float('42.9')}"
    expected_as_int = f"as_int={int(float('42.9'))}"

    assert out[0] == expected_text, f"expected={expected_text} actual={out[0]}"
    assert out[1] == expected_as_float, f"expected={expected_as_float} actual={out[1]}"
    assert out[2] == expected_as_int, f"expected={expected_as_int} actual={out[2]}"


def test_negative_value(monkeypatch, capsys):
    mod, out = run_script(monkeypatch, capsys, "-2.1")
    assert isinstance(mod.as_float, float)
    assert isinstance(mod.as_int, int)

    expected = [
        "text=-2.1",
        f"as_float={float('-2.1')}",
        f"as_int={int(float('-2.1'))}",
    ]
    for i in range(3):
        assert out[i] == expected[i], f"expected={expected[i]} actual={out[i]}"


def test_integer_input_string(monkeypatch, capsys):
    mod, out = run_script(monkeypatch, capsys, "7")
    assert isinstance(mod.as_float, float)
    assert isinstance(mod.as_int, int)

    expected = [
        "text=7",
        f"as_float={float('7')}",
        f"as_int={int(float('7'))}",
    ]
    for i in range(3):
        assert out[i] == expected[i], f"expected={expected[i]} actual={out[i]}"


def test_whitespace_input_preserved_in_text_but_numeric_conversion_works(monkeypatch, capsys):
    mod, out = run_script(monkeypatch, capsys, "  3.5 ")
    assert out[0] == "text=  3.5 "
    assert isinstance(mod.as_float, float)
    assert isinstance(mod.as_int, int)

    expected_as_float = f"as_float={float('  3.5 ')}"
    expected_as_int = f"as_int={int(float('  3.5 '))}"
    assert out[1] == expected_as_float, f"expected={expected_as_float} actual={out[1]}"
    assert out[2] == expected_as_int, f"expected={expected_as_int} actual={out[2]}"