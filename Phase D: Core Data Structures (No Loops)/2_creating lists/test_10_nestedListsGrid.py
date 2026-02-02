import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout

MODULE_FILE = "10_nestedListsGrid.py"


def load_module():
    spec = importlib.util.spec_from_file_location("nestedListsGrid10", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            spec.loader.exec_module(module)
    except Exception as e:
        raise AssertionError(f"import error: expected no exception, actual {type(e).__name__}") from e
    return module, f.getvalue()


def parse_last_printed_obj(stdout_text):
    lines = [ln.strip() for ln in stdout_text.splitlines() if ln.strip() != ""]
    if not lines:
        raise AssertionError("stdout: expected at least one printed line, actual none")
    last = lines[-1]
    try:
        return ast.literal_eval(last)
    except Exception as e:
        raise AssertionError(f"stdout parse: expected Python literal list, actual {last!r}") from e


def test_module_imports_without_error():
    load_module()


def test_grid_exists_and_is_list_of_lists():
    module, _ = load_module()
    assert hasattr(module, "grid"), "grid: expected defined, actual missing"
    grid = module.grid
    assert isinstance(grid, list), f"grid type: expected list, actual {type(grid).__name__}"
    assert len(grid) == 3, f"grid rows: expected 3, actual {len(grid)}"
    assert all(isinstance(r, list) for r in grid), "grid rows type: expected all lists, actual not all lists"
    lengths = [len(r) for r in grid]
    assert all(l == 4 for l in lengths), f"grid cols: expected all 4, actual {lengths}"


def test_grid_filled_with_underscores():
    module, _ = load_module()
    grid = module.grid
    vals = [cell for row in grid for cell in row]
    expected = ["_"] * 12
    assert vals == expected, f"grid values: expected {expected}, actual {vals}"


def test_rows_are_distinct_objects():
    module, _ = load_module()
    grid = module.grid
    row_ids = [id(r) for r in grid]
    assert len(set(row_ids)) == 3, f"row identity: expected 3 distinct, actual {len(set(row_ids))}"


def test_prints_grid():
    module, stdout = load_module()
    printed_obj = parse_last_printed_obj(stdout)
    assert printed_obj == module.grid, f"print: expected {module.grid}, actual {printed_obj}"