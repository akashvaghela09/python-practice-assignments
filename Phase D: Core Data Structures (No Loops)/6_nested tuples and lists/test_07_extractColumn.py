import importlib.util
import io
import os
import sys
import ast
import contextlib

FILE_NAME = "07_extractColumn.py"


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("mod_07_extractColumn", path)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_printed_output_exact(tmp_path):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    _, out = _run_script_capture_stdout(path)
    assert out == "[2, 5, 8]\n", f"expected '[2, 5, 8]\\n' vs actual {out!r}"


def test_column_variable_matches_print(tmp_path):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    mod, out = _run_script_capture_stdout(path)
    printed = ast.literal_eval(out.strip())
    assert getattr(mod, "column") == printed, f"expected {printed!r} vs actual {getattr(mod, 'column')!r}"


def test_column_is_list_of_ints(tmp_path):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    mod, _ = _run_script_capture_stdout(path)
    col = getattr(mod, "column")
    assert isinstance(col, list), f"expected {list!r} vs actual {type(col)!r}"
    assert all(isinstance(x, int) for x in col), f"expected all {int!r} vs actual {[type(x) for x in col]!r}"


def test_column_values_derived_from_matrix_and_index(tmp_path):
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    mod, _ = _run_script_capture_stdout(path)
    expected = [row[getattr(mod, "col_index")] for row in getattr(mod, "matrix")]
    actual = getattr(mod, "column")
    assert actual == expected, f"expected {expected!r} vs actual {actual!r}"