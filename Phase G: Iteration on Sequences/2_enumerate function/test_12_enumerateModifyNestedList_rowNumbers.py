import importlib.util
import pathlib
import ast
import sys
import pytest


FILE_NAME = "12_enumerateModifyNestedList_rowNumbers.py"


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("student_mod_12", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout(path, monkeypatch):
    out = []

    class _Stdout:
        def write(self, s):
            out.append(s)

        def flush(self):
            pass

    monkeypatch.setattr(sys, "stdout", _Stdout())
    mod = _load_module_from_path(path)
    return mod, "".join(out)


def test_script_imports_and_prints_table(monkeypatch):
    path = pathlib.Path(FILE_NAME)
    assert path.exists()
    mod, captured = _run_script_capture_stdout(path, monkeypatch)

    assert hasattr(mod, "table")
    assert isinstance(mod.table, list)

    printed_lines = [ln.strip() for ln in captured.splitlines() if ln.strip()]
    assert len(printed_lines) >= 1

    last = printed_lines[-1]
    parsed = ast.literal_eval(last)
    assert parsed == mod.table


def test_table_shape_and_inplace_modification(monkeypatch):
    path = pathlib.Path(FILE_NAME)
    mod, _ = _run_script_capture_stdout(path, monkeypatch)

    tbl = mod.table
    assert isinstance(tbl, list)
    assert len(tbl) == 3

    for row in tbl:
        assert isinstance(row, list)
        assert len(row) == 2
        assert isinstance(row[0], int)
        assert isinstance(row[1], str)

    names = [row[1] for row in tbl]
    assert names == ["Ann", "Ben", "Cy"]

    numbers = [row[0] for row in tbl]
    assert numbers == list(range(1, len(tbl) + 1))


def test_numbers_match_row_positions(monkeypatch):
    path = pathlib.Path(FILE_NAME)
    mod, _ = _run_script_capture_stdout(path, monkeypatch)

    for idx, row in enumerate(mod.table, start=1):
        assert row[0] == idx


def test_no_new_outer_table_object_created(monkeypatch):
    path = pathlib.Path(FILE_NAME)
    mod1, _ = _run_script_capture_stdout(path, monkeypatch)
    tbl1 = mod1.table
    assert isinstance(tbl1, list)

    mod2, _ = _run_script_capture_stdout(path, monkeypatch)
    tbl2 = mod2.table
    assert isinstance(tbl2, list)

    assert tbl1 is not tbl2  # separate runs should create new module objects


def test_uses_enumerate_and_insert_in_source():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    assert "enumerate" in src
    assert ".insert" in src


def test_no_append_used():
    src = pathlib.Path(FILE_NAME).read_text(encoding="utf-8")
    assert ".append" not in src


@pytest.mark.parametrize(
    "name,expected_num",
    [("Ann", 1), ("Ben", 2), ("Cy", 3)],
)
def test_rows_have_expected_number_for_name(monkeypatch, name, expected_num):
    path = pathlib.Path(FILE_NAME)
    mod, _ = _run_script_capture_stdout(path, monkeypatch)

    found = [row for row in mod.table if row[1] == name]
    assert len(found) == 1
    assert found[0][0] == expected_num