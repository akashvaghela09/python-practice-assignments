import ast
import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout


def _load_module(path, module_name="assignment_mod"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_output(path):
    buf = io.StringIO()
    spec = importlib.util.spec_from_file_location("assignment_run", path)
    mod = importlib.util.module_from_spec(spec)
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return buf.getvalue(), mod


def _expected_from_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def test_printed_output_matches_expected():
    path = os.path.join(os.path.dirname(__file__), "14_transposeMatrix.py")
    out, mod = _run_script_capture_output(path)
    expected_obj = _expected_from_matrix(mod.matrix)
    expected = str(expected_obj) + "\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_transposed_value_correct_and_shape():
    path = os.path.join(os.path.dirname(__file__), "14_transposeMatrix.py")
    mod = _load_module(path, "assignment_value")
    expected = _expected_from_matrix(mod.matrix)
    assert mod.transposed == expected, f"expected={expected!r} actual={mod.transposed!r}"
    assert isinstance(mod.transposed, list), f"expected={list!r} actual={type(mod.transposed)!r}"
    assert all(isinstance(r, list) for r in mod.transposed), f"expected={'list rows'!r} actual={mod.transposed!r}"
    assert len(mod.transposed) == len(mod.matrix[0]), f"expected={len(mod.matrix[0])!r} actual={len(mod.transposed)!r}"
    assert all(len(r) == len(mod.matrix) for r in mod.transposed), f"expected={len(mod.matrix)!r} actual={[len(r) for r in mod.transposed]!r}"


def test_transposed_not_none_and_not_aliasing_rows():
    path = os.path.join(os.path.dirname(__file__), "14_transposeMatrix.py")
    mod = _load_module(path, "assignment_alias")
    assert mod.transposed is not None, f"expected={True!r} actual={(mod.transposed is not None)!r}"
    if isinstance(mod.transposed, list) and all(isinstance(r, list) for r in mod.transposed) and len(mod.transposed) > 1:
        assert len({id(r) for r in mod.transposed}) == len(mod.transposed), f"expected={len(mod.transposed)!r} actual={len({id(r) for r in mod.transposed})!r}"


def test_source_does_not_set_transposed_none():
    path = os.path.join(os.path.dirname(__file__), "14_transposeMatrix.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    assigns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "transposed":
                    assigns.append(node.value)
    has_none_assignment = any(isinstance(v, ast.Constant) and v.value is None for v in assigns)
    assert not has_none_assignment, f"expected={False!r} actual={has_none_assignment!r}"