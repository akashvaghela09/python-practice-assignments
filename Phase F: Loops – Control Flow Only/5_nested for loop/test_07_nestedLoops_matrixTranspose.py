import importlib.util
import os
import sys


def _load_module_with_capture(module_name, file_name):
    path = os.path.join(os.path.dirname(__file__), file_name)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    captured = {"printed": []}

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured["printed"].append(sep.join(str(a) for a in args) + end)

    module.print = fake_print
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module, captured


def test_transpose_is_correct_and_not_empty():
    mod, _ = _load_module_with_capture("student_mod_07_a", "07_nestedLoops_matrixTranspose.py")
    expected = [[1, 4], [2, 5], [3, 6]]
    assert hasattr(mod, "transpose")
    assert mod.transpose != [], f"expected {expected} vs actual {mod.transpose}"
    assert mod.transpose == expected, f"expected {expected} vs actual {mod.transpose}"


def test_transpose_dimensions_match_cols_by_rows():
    mod, _ = _load_module_with_capture("student_mod_07_b", "07_nestedLoops_matrixTranspose.py")
    expected_rows = len(mod.matrix[0])
    expected_cols = len(mod.matrix)
    assert isinstance(mod.transpose, list)
    assert len(mod.transpose) == expected_rows, f"expected {expected_rows} vs actual {len(mod.transpose)}"
    assert all(isinstance(r, list) for r in mod.transpose)
    for r in mod.transpose:
        assert len(r) == expected_cols, f"expected {expected_cols} vs actual {len(r)}"


def test_transpose_matches_generic_nested_loop_computation():
    mod, _ = _load_module_with_capture("student_mod_07_c", "07_nestedLoops_matrixTranspose.py")
    m = mod.matrix
    rows = len(m)
    cols = len(m[0])
    expected = []
    for c in range(cols):
        new_row = []
        for r in range(rows):
            new_row.append(m[r][c])
        expected.append(new_row)

    assert mod.transpose == expected, f"expected {expected} vs actual {mod.transpose}"


def test_prints_transpose_value():
    mod, captured = _load_module_with_capture("student_mod_07_d", "07_nestedLoops_matrixTranspose.py")
    expected = str(mod.transpose)
    printed = "".join(captured["printed"]).strip()
    assert printed != "", f"expected {expected} vs actual {printed}"
    assert printed == expected, f"expected {expected} vs actual {printed}"


def test_transpose_is_not_the_same_object_as_matrix():
    mod, _ = _load_module_with_capture("student_mod_07_e", "07_nestedLoops_matrixTranspose.py")
    assert mod.transpose is not mod.matrix, f"expected {id(mod.matrix)} vs actual {id(mod.transpose)}"