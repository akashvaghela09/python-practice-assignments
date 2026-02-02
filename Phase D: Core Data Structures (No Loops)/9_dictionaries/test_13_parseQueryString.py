import importlib.util
import pathlib
import ast
import pytest


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "13_parseQueryString.py"
    spec = importlib.util.spec_from_file_location("parse_query_mod", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_params_is_dict():
    mod = load_module()
    assert isinstance(mod.params, dict), f"expected dict, got {type(mod.params)!r}"


def test_params_matches_expected_structure_and_values():
    mod = load_module()
    expected = {"lang": "py", "level": "2", "mode": "practice"}
    assert mod.params == expected, f"expected {expected!r}, got {mod.params!r}"


def test_params_values_are_strings():
    mod = load_module()
    non_str = {k: v for k, v in mod.params.items() if not isinstance(v, str)}
    assert not non_str, f"expected all str values, got {non_str!r}"


def test_query_not_mutated():
    mod = load_module()
    expected_query = "lang=py&level=2&mode=practice"
    assert mod.query == expected_query, f"expected {expected_query!r}, got {mod.query!r}"


def test_prints_params_dict(capsys):
    load_module()
    out = capsys.readouterr().out.strip()
    expected = {"lang": "py", "level": "2", "mode": "practice"}
    try:
        actual = ast.literal_eval(out)
    except Exception:
        pytest.fail(f"expected {expected!r}, got {out!r}")
    assert actual == expected, f"expected {expected!r}, got {actual!r}"