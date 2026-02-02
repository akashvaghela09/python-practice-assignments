import ast
import importlib.util
import os
import sys


def _module_path():
    return os.path.join(os.path.dirname(__file__), "04_replaceMultipleByLoopWithIndex.py")


def _run_module_capture_stdout(path):
    import io
    import contextlib

    buf = io.StringIO()
    spec = importlib.util.spec_from_file_location("student_mod_04", path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def _parse_printed_list(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        return ast.literal_eval(last)
    except Exception:
        return None


def test_replaces_all_minus_one_with_zero_and_prints_expected():
    path = _module_path()
    mod, out = _run_module_capture_stdout(path)

    assert hasattr(mod, "nums")

    actual_list = mod.nums
    printed_list = _parse_printed_list(out)

    expected = [1, 0, 2, 0, 3, 0]

    assert printed_list == expected, f"expected={expected!r} actual={printed_list!r}"
    assert actual_list == expected, f"expected={expected!r} actual={actual_list!r}"


def test_no_minus_one_remains():
    path = _module_path()
    mod, _ = _run_module_capture_stdout(path)

    assert -1 not in mod.nums, f"expected={False!r} actual={(-1 in mod.nums)!r}"


def test_list_length_unchanged():
    path = _module_path()
    mod, _ = _run_module_capture_stdout(path)

    expected_len = 6
    actual_len = len(mod.nums)
    assert actual_len == expected_len, f"expected={expected_len!r} actual={actual_len!r}"


def test_uses_for_loop_over_indexes_not_list_comprehension():
    path = _module_path()
    src = open(path, "r", encoding="utf-8").read()
    tree = ast.parse(src)

    has_for = any(isinstance(n, ast.For) for n in ast.walk(tree))
    assert has_for is True, f"expected={True!r} actual={has_for!r}"

    has_listcomp = any(isinstance(n, ast.ListComp) for n in ast.walk(tree))
    assert has_listcomp is False, f"expected={False!r} actual={has_listcomp!r}"

    has_slice_assign = any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Slice) for t in n.targets) for n in ast.walk(tree))
    assert has_slice_assign is False, f"expected={False!r} actual={has_slice_assign!r}"