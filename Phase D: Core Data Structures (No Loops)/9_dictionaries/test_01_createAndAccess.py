import importlib.util
import os
import sys
import re


def _load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(path, module_name="assignment_mod"):
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        _load_module_from_path(module_name, path)
    return buf.getvalue()


def test_outputs_id_and_name_in_order():
    path = os.path.join(os.path.dirname(__file__), "01_createAndAccess.py")
    out = _run_script_capture_stdout(path, module_name="mod_out_1")
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected 2 lines, actual {len(lines)}"
    assert re.fullmatch(r"\d+", lines[0]) is not None, f"expected numeric id, actual {lines[0]!r}"
    assert lines[1] != "", f"expected non-empty name, actual {lines[1]!r}"


def test_employee_dictionary_has_required_keys_and_types():
    path = os.path.join(os.path.dirname(__file__), "01_createAndAccess.py")
    mod = _load_module_from_path("mod_emp_1", path)

    assert hasattr(mod, "employee"), "expected employee defined, actual missing"
    assert isinstance(mod.employee, dict), f"expected dict, actual {type(mod.employee).__name__}"

    assert "id" in mod.employee, f"expected key 'id' present, actual keys {sorted(mod.employee.keys())}"
    assert "name" in mod.employee, f"expected key 'name' present, actual keys {sorted(mod.employee.keys())}"

    assert isinstance(mod.employee["id"], int), f"expected id int, actual {type(mod.employee['id']).__name__}"
    assert isinstance(mod.employee["name"], str), f"expected name str, actual {type(mod.employee['name']).__name__}"
    assert mod.employee["name"] != "", "expected non-empty name, actual empty"


def test_first_print_matches_employee_id_and_second_matches_employee_name():
    path = os.path.join(os.path.dirname(__file__), "01_createAndAccess.py")
    mod = _load_module_from_path("mod_emp_2", path)
    out = _run_script_capture_stdout(path, module_name="mod_out_2")
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected 2 lines, actual {len(lines)}"

    expected_id = str(mod.employee["id"])
    expected_name = str(mod.employee["name"])
    assert lines[0] == expected_id, f"expected {expected_id!r}, actual {lines[0]!r}"
    assert lines[1] == expected_name, f"expected {expected_name!r}, actual {lines[1]!r}"