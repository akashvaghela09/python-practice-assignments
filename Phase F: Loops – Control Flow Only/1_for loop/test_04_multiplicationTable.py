import importlib.util
import os
import sys
import pytest


def _load_module_from_path(path, module_name="student_mod"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected_output():
    lines = []
    n = 7
    for i in range(1, 6):
        lines.append(f"{n} x {i} = {n*i}")
    return "\n".join(lines) + "\n"


def test_file_exists():
    assert os.path.exists("04_multiplicationTable.py")


def test_import_runs_without_syntax_error():
    path = os.path.abspath("04_multiplicationTable.py")
    try:
        _load_module_from_path(path, "mod_import_check")
    except SyntaxError as e:
        pytest.fail(f"expected: import succeeds; actual: SyntaxError {e.msg}")


def test_prints_exact_times_table_output(capsys):
    path = os.path.abspath("04_multiplicationTable.py")
    _load_module_from_path(path, "mod_run_output")
    captured = capsys.readouterr()
    expected = _expected_output()
    actual = captured.out
    assert actual == expected, f"expected: {expected!r}; actual: {actual!r}"


def test_no_extra_stderr(capsys):
    path = os.path.abspath("04_multiplicationTable.py")
    _load_module_from_path(path, "mod_run_stderr")
    captured = capsys.readouterr()
    expected = ""
    actual = captured.err
    assert actual == expected, f"expected: {expected!r}; actual: {actual!r}"