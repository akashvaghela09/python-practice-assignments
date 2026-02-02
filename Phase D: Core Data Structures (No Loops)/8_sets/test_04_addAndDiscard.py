import ast
import importlib.util
import pathlib
import re

import pytest


FILE_NAME = "04_addAndDiscard.py"


def _load_module(tmp_path, source):
    p = tmp_path / FILE_NAME
    p.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_mod", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_source():
    path = pathlib.Path(FILE_NAME)
    return path.read_text(encoding="utf-8")


def test_no_placeholders():
    src = _read_source()
    assert "____" not in src


def test_set_operations_present():
    src = _read_source()
    tree = ast.parse(src)

    add_calls = []
    discard_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "letters":
                if node.func.attr == "add":
                    add_calls.append(node)
                if node.func.attr == "discard":
                    discard_calls.append(node)

    assert len(add_calls) >= 1
    assert len(discard_calls) >= 1

    add_arg_ok = any(
        len(c.args) == 1 and isinstance(c.args[0], ast.Constant) and c.args[0].value == "d"
        for c in add_calls
    )
    discard_arg_ok = any(
        len(c.args) == 1 and isinstance(c.args[0], ast.Constant) and c.args[0].value == "b"
        for c in discard_calls
    )

    assert add_arg_ok
    assert discard_arg_ok


def test_output_is_expected_set(capsys):
    spec = importlib.util.spec_from_file_location("mod_run", FILE_NAME)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out = capsys.readouterr().out.strip()
    assert out

    m = re.fullmatch(r"\{.*\}", out)
    assert m

    parsed = ast.literal_eval(out)
    assert isinstance(parsed, set)

    expected = {"a", "c", "d"}
    assert parsed == expected, f"expected={expected} actual={parsed}"


def test_letters_variable_final_value():
    spec = importlib.util.spec_from_file_location("mod_run2", FILE_NAME)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    expected = {"a", "c", "d"}
    actual = getattr(mod, "letters", None)
    assert actual == expected, f"expected={expected} actual={actual}"