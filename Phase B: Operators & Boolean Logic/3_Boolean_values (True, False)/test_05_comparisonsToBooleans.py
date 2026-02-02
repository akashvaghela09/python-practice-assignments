import importlib.util
import pathlib
import sys
import pytest


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "05_comparisonsToBooleans.py"
    spec = importlib.util.spec_from_file_location("comparisonsToBooleans_05", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_variables_exist_and_are_booleans():
    m = load_module()
    assert hasattr(m, "is_adult")
    assert hasattr(m, "passed")
    assert isinstance(m.is_adult, bool), f"expected={bool} actual={type(m.is_adult)}"
    assert isinstance(m.passed, bool), f"expected={bool} actual={type(m.passed)}"


def test_is_adult_logic():
    m = load_module()
    expected = (m.age >= m.min_age)
    assert m.is_adult == expected, f"expected={expected} actual={m.is_adult}"


def test_passed_logic():
    m = load_module()
    expected = (m.score >= m.passing_score)
    assert m.passed == expected, f"expected={expected} actual={m.passed}"


def test_expected_print_output(capsys):
    load_module()
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 2, f"expected={2} actual={len(out)}"
    assert out[0] in ("True", "False"), f"expected={('True','False')} actual={out[0]}"
    assert out[1] in ("True", "False"), f"expected={('True','False')} actual={out[1]}"