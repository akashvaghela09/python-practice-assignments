import importlib.util
import os
import sys
import types
import pytest

MODULE_FILENAME = "15_nested_ternary_with_three_way_choice.py"


def load_module(tmp_path, source_text):
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(source_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_mod", str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["student_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_module_capture_stdout(tmp_path, source_text, monkeypatch):
    file_path = tmp_path / MODULE_FILENAME
    file_path.write_text(source_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_mod_run", str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["student_mod_run"] = mod

    out = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: out.append(" ".join(map(str, a))))
    spec.loader.exec_module(mod)
    return mod, "\n".join(out)


def test_importable_and_prints_only_zero(tmp_path, monkeypatch):
    source_path = os.path.join(os.getcwd(), MODULE_FILENAME)
    assert os.path.exists(source_path), f"missing:{MODULE_FILENAME}"
    source = open(source_path, "r", encoding="utf-8").read()

    mod, printed = run_module_capture_stdout(tmp_path, source, monkeypatch)
    expected = "zero"
    actual = printed
    assert actual == expected, f"expected:{expected} actual:{actual}"


def test_category_exists_and_matches_output(tmp_path, monkeypatch):
    source_path = os.path.join(os.getcwd(), MODULE_FILENAME)
    source = open(source_path, "r", encoding="utf-8").read()

    mod, printed = run_module_capture_stdout(tmp_path, source, monkeypatch)
    assert hasattr(mod, "category"), "missing:category"
    expected = getattr(mod, "category")
    actual = printed
    assert actual == expected, f"expected:{expected} actual:{actual}"


def test_uses_ternary_expression_not_if_statement():
    source_path = os.path.join(os.getcwd(), MODULE_FILENAME)
    source = open(source_path, "r", encoding="utf-8").read()

    compact = "\n".join(line.split("#", 1)[0] for line in source.splitlines())
    assert " if " in compact and " else " in compact
    assert "\nif " not in compact and "\nelif " not in compact and "\nelse" not in compact


def test_not_left_blank_placeholders():
    source_path = os.path.join(os.getcwd(), MODULE_FILENAME)
    source = open(source_path, "r", encoding="utf-8").read()

    assert "________________" not in source