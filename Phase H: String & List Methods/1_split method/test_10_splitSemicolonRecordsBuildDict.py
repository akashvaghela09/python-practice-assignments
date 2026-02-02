import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILE = "10_splitSemicolonRecordsBuildDict.py"
MODULE_NAME = "split_semicolon_records_build_dict_10"


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_module_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(path)
    return buf.getvalue()


def _parse_last_dict_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        raise AssertionError("expected: dict printed, actual: <no output>")
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        raise AssertionError(f"expected: dict literal, actual: {last!r}")
    if not isinstance(val, dict):
        raise AssertionError(f"expected: dict, actual: {type(val).__name__}")
    return val


def test_runs_without_placeholder_tokens():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "___" not in src, f"expected: no placeholders, actual: placeholders present"


def test_prints_dictionary_with_expected_keys_and_values():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    out = _run_module_capture_stdout(path)
    d = _parse_last_dict_from_stdout(out)

    expected = {"name": "Ada", "lang": "Python", "year": "2026"}
    assert d == expected, f"expected: {expected!r}, actual: {d!r}"


def test_result_variable_is_dict_with_expected_content():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    module = _load_module_from_path(path)
    assert hasattr(module, "result"), "expected: result defined, actual: missing"
    assert isinstance(module.result, dict), f"expected: dict, actual: {type(module.result).__name__}"

    expected = {"name": "Ada", "lang": "Python", "year": "2026"}
    assert module.result == expected, f"expected: {expected!r}, actual: {module.result!r}"


def test_records_and_split_logic_produces_three_records():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    module = _load_module_from_path(path)

    assert hasattr(module, "records"), "expected: records defined, actual: missing"
    assert isinstance(module.records, list), f"expected: list, actual: {type(module.records).__name__}"
    assert len(module.records) == 3, f"expected: 3, actual: {len(module.records)!r}"

    for rec in module.records:
        assert isinstance(rec, str), f"expected: str, actual: {type(rec).__name__}"
        assert ":" in rec, f"expected: contains ':', actual: {rec!r}"
        assert rec.count(":") == 1, f"expected: 1, actual: {rec.count(':')!r}"


def test_text_unchanged_and_expected_format():
    path = os.path.join(os.getcwd(), MODULE_FILE)
    module = _load_module_from_path(path)

    assert hasattr(module, "text"), "expected: text defined, actual: missing"
    assert isinstance(module.text, str), f"expected: str, actual: {type(module.text).__name__}"

    expected_text = "name:Ada;lang:Python;year:2026"
    assert module.text == expected_text, f"expected: {expected_text!r}, actual: {module.text!r}"