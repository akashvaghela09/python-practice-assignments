import importlib
import sys
from pathlib import Path


def _run_code_with_globals(code: str, g: dict):
    compiled = compile(code, "02_eitherCondition.py", "exec")
    exec(compiled, g, g)


def _expected_output(age: int, has_permission: bool) -> str:
    return "ELIGIBLE\n" if (age >= 18 or has_permission is True) else "NOT ELIGIBLE\n"


def _load_source():
    p = Path(__file__).resolve().parent / "02_eitherCondition.py"
    return p.read_text(encoding="utf-8")


def test_runs_without_placeholder_syntax_error():
    src = _load_source()
    g = {}
    try:
        _run_code_with_globals(src, g)
    except SyntaxError as e:
        raise AssertionError(f"expected: no SyntaxError, actual: {type(e).__name__}")


def test_expected_output_default_values(capsys):
    mod = importlib.import_module("02_eitherCondition")
    out = capsys.readouterr().out
    exp = _expected_output(getattr(mod, "age"), getattr(mod, "has_permission"))
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_age16_permission_true_prints_eligible(capsys):
    src = _load_source()
    g = {"age": 16, "has_permission": True}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(16, True)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_age16_permission_false_prints_not_eligible(capsys):
    src = _load_source()
    g = {"age": 16, "has_permission": False}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(16, False)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_age18_permission_false_prints_eligible(capsys):
    src = _load_source()
    g = {"age": 18, "has_permission": False}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(18, False)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_age17_permission_false_prints_not_eligible(capsys):
    src = _load_source()
    g = {"age": 17, "has_permission": False}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(17, False)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_age19_permission_false_prints_eligible(capsys):
    src = _load_source()
    g = {"age": 19, "has_permission": False}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(19, False)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_has_permission_truthy_non_bool_not_treated_as_true(capsys):
    src = _load_source()
    g = {"age": 16, "has_permission": 1}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(16, 1)
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_has_permission_string_true_not_treated_as_true(capsys):
    src = _load_source()
    g = {"age": 16, "has_permission": "True"}
    _run_code_with_globals(src, g)
    out = capsys.readouterr().out
    exp = _expected_output(16, "True")
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"


def test_import_is_repeatable(monkeypatch, capsys):
    if "02_eitherCondition" in sys.modules:
        del sys.modules["02_eitherCondition"]
    importlib.import_module("02_eitherCondition")
    capsys.readouterr()

    if "02_eitherCondition" in sys.modules:
        del sys.modules["02_eitherCondition"]
    importlib.import_module("02_eitherCondition")
    out = capsys.readouterr().out

    mod = importlib.import_module("02_eitherCondition")
    exp = _expected_output(getattr(mod, "age"), getattr(mod, "has_permission"))
    assert out == exp, f"expected: {exp!r}, actual: {out!r}"