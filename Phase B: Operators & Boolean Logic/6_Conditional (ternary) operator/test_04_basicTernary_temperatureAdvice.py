import importlib.util
import pathlib
import sys
import re

import pytest


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_freeze_exactly(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "04_basicTernary_temperatureAdvice.py"
    module_name = "assignment_04_basicTernary_temperatureAdvice"
    if module_name in sys.modules:
        del sys.modules[module_name]
    _load_module(module_name, file_path)
    out = capsys.readouterr().out
    expected = "freeze\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_uses_ternary_and_not_if_statement():
    file_path = pathlib.Path(__file__).resolve().parent / "04_basicTernary_temperatureAdvice.py"
    src = file_path.read_text(encoding="utf-8")

    has_ternary = bool(re.search(r"\bmessage\s*=\s*.+\s+if\s+.+\s+else\s+.+", src, flags=re.DOTALL))
    assert has_ternary, "expected=ternary actual=missing"

    has_if_stmt = bool(re.search(r"^\s*if\b", src, flags=re.MULTILINE))
    assert not has_if_stmt, "expected=no_if_statement actual=found_if_statement"


def test_no_placeholder_underscores_left():
    file_path = pathlib.Path(__file__).resolve().parent / "04_basicTernary_temperatureAdvice.py"
    src = file_path.read_text(encoding="utf-8")
    has_placeholder = "________________" in src
    assert not has_placeholder, "expected=no_placeholder actual=placeholder_present"