import ast
import importlib.util
import os
import sys


def _load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_assignment_path():
    here = os.path.dirname(__file__)
    return os.path.join(here, "11_swapPairsInPlace.py")


def test_file_imports_cleanly():
    path = _get_assignment_path()
    assert os.path.exists(path)
    _load_module_from_path("swap_pairs_inplace_mod", path)


def test_printed_output_matches_expected(capsys):
    path = _get_assignment_path()
    _load_module_from_path("swap_pairs_inplace_mod_out", path)
    out = capsys.readouterr().out.strip()
    expected = "['b', 'a', 'd', 'c', 'e']"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_items_list_matches_expected_after_execution():
    path = _get_assignment_path()
    mod = _load_module_from_path("swap_pairs_inplace_mod_items", path)
    expected = ["b", "a", "d", "c", "e"]
    actual = getattr(mod, "items", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_swaps_done_in_place_same_list_object():
    path = _get_assignment_path()
    mod = _load_module_from_path("swap_pairs_inplace_mod_inplace", path)
    items_obj = getattr(mod, "items", None)
    assert isinstance(items_obj, list)
    original_id = id(items_obj)

    assert id(items_obj) == original_id


def test_source_uses_indices_and_tuple_swap():
    path = _get_assignment_path()
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    for_loops = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_loops) >= 1

    found_range_step2 = False
    for n in for_loops:
        it = n.iter
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == "range":
            if len(it.args) == 3:
                step = it.args[2]
                if isinstance(step, ast.Constant) and step.value == 2:
                    found_range_step2 = True
                    break
    assert found_range_step2

    found_tuple_swap = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            tgt = n.targets[0]
            if isinstance(tgt, ast.Tuple) and isinstance(n.value, ast.Tuple):
                if len(tgt.elts) == 2 and len(n.value.elts) == 2:
                    left, right = tgt.elts
                    v1, v2 = n.value.elts
                    if (
                        isinstance(left, ast.Subscript)
                        and isinstance(right, ast.Subscript)
                        and isinstance(v1, ast.Subscript)
                        and isinstance(v2, ast.Subscript)
                    ):
                        found_tuple_swap = True
                        break
    assert found_tuple_swap


def test_does_not_change_length_or_elements_set():
    path = _get_assignment_path()
    mod = _load_module_from_path("swap_pairs_inplace_mod_integrity", path)
    actual = mod.items
    expected_set = {"a", "b", "c", "d", "e"}
    assert len(actual) == 5, f"expected={5!r} actual={len(actual)!r}"
    assert set(actual) == expected_set, f"expected={expected_set!r} actual={set(actual)!r}"