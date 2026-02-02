import importlib.util
import pathlib
import sys
import pytest


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_module_imports_without_syntax_error():
    file_path = pathlib.Path(__file__).resolve().parent / "07_nestedGrid.py"
    assert file_path.exists()
    _load_module("nestedGrid07_import_test", file_path)


def test_printed_grid_exact_output(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "07_nestedGrid.py"
    try:
        _load_module("nestedGrid07_output_test", file_path)
    except Exception as e:
        pytest.fail(f"expected=<module runs without error> actual=<{type(e).__name__}: {e}>")

    out = capsys.readouterr().out
    expected = "****\n****\n****\n"
    assert out == expected, f"expected=<{expected!r}> actual=<{out!r}>"


def test_printed_grid_has_3_lines_each_4_chars(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "07_nestedGrid.py"
    try:
        _load_module("nestedGrid07_structure_test", file_path)
    except Exception as e:
        pytest.fail(f"expected=<module runs without error> actual=<{type(e).__name__}: {e}>")

    out = capsys.readouterr().out
    lines = out.splitlines()
    expected_lines = 3
    assert len(lines) == expected_lines, f"expected=<{expected_lines}> actual=<{len(lines)}>"
    for i, line in enumerate(lines):
        expected_len = 4
        assert len(line) == expected_len, f"expected=<{expected_len}> actual=<{len(line)}>"
        expected_set = {"*"}
        actual_set = set(line)
        assert actual_set == expected_set, f"expected=<{expected_set}> actual=<{actual_set}>"