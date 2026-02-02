import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "01_tupleCreationAndIndexing.py"


def load_module_from_path(path):
    module_name = "student_module_01_tupleCreationAndIndexing"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout(path):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        load_module_from_path(path)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


def test_file_exists():
    assert os.path.exists(MODULE_FILENAME)


def test_runs_without_exception():
    run_script_capture_stdout(MODULE_FILENAME)


def test_coords_is_tuple_of_two_ints():
    m = load_module_from_path(MODULE_FILENAME)
    assert hasattr(m, "coords")
    assert isinstance(m.coords, tuple)
    assert len(m.coords) == 2
    assert all(isinstance(x, int) for x in m.coords)


def test_coords_values_and_print_output_order():
    out = run_script_capture_stdout(MODULE_FILENAME)
    m = load_module_from_path(MODULE_FILENAME)

    expected_lines = [str(m.coords[0]), str(m.coords[1])]
    actual_lines = [line.rstrip("\n") for line in out.splitlines()]

    assert expected_lines == actual_lines, f"expected={expected_lines} actual={actual_lines}"


def test_prints_exactly_two_lines():
    out = run_script_capture_stdout(MODULE_FILENAME)
    lines = out.splitlines()
    assert 2 == len(lines), f"expected={2} actual={len(lines)}"


def test_coords_exact_values():
    m = load_module_from_path(MODULE_FILENAME)
    expected = (10, 20)
    actual = m.coords
    assert expected == actual, f"expected={expected} actual={actual}"