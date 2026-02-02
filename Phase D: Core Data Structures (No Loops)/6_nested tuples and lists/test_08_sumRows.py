import importlib
import io
import contextlib
import ast
import pytest

MODULE_NAME = "08_sumRows"

def run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()

def parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    if not lines:
        raise AssertionError(f"expected output vs actual output: {repr('[...]')} vs {repr(out)}")
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        raise AssertionError(f"expected output vs actual output: {repr('[...]')} vs {repr(last)}")
    if not isinstance(val, list):
        raise AssertionError(f"expected output vs actual output: {repr('list')} vs {repr(type(val).__name__)}")
    return val

def test_prints_expected_row_sums(capsys):
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    mod, out = run_module_capture_stdout()
    printed = parse_last_list_from_stdout(out)
    expected = [sum(row) for row in mod.matrix]
    assert printed == expected, f"expected vs actual: {expected} vs {printed}"

def test_row_sums_variable_matches_printed_and_is_list():
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    mod, out = run_module_capture_stdout()
    printed = parse_last_list_from_stdout(out)
    assert isinstance(mod.row_sums, list), f"expected vs actual: {'list'} vs {type(mod.row_sums).__name__}"
    assert mod.row_sums == printed, f"expected vs actual: {printed} vs {mod.row_sums}"

def test_row_sums_correct_for_each_row():
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    mod, out = run_module_capture_stdout()
    expected = [sum(row) for row in mod.matrix]
    assert mod.row_sums == expected, f"expected vs actual: {expected} vs {mod.row_sums}"

def test_row_sums_length_matches_number_of_rows():
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    mod, out = run_module_capture_stdout()
    assert len(mod.row_sums) == len(mod.matrix), f"expected vs actual: {len(mod.matrix)} vs {len(mod.row_sums)}"