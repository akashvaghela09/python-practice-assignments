import importlib
import ast
import io
import contextlib
import inspect
import re

mod = importlib.import_module("02_sliceAssignment")


def _run_main_capture():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main()
    return buf.getvalue()


def test_main_prints_expected_list_only():
    out = _run_main_capture()
    expected = "[1, 2, 7, 8, 5]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_uses_slice_assignment_not_item_by_item():
    src = inspect.getsource(mod)
    tree = ast.parse(src)

    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    slice_assigns = []
    for a in assigns:
        for t in a.targets:
            if isinstance(t, ast.Subscript):
                s = t.slice
                if isinstance(s, ast.Slice):
                    slice_assigns.append(a)
                elif isinstance(s, ast.Tuple) and any(isinstance(elt, ast.Slice) for elt in s.elts):
                    slice_assigns.append(a)

    assert len(slice_assigns) >= 1, f"expected>={1!r} actual={len(slice_assigns)!r}"

    # Ensure not doing direct element replacement for indices 2 and 3
    subscript_index_assigns = []
    for a in assigns:
        for t in a.targets:
            if isinstance(t, ast.Subscript):
                s = t.slice
                if isinstance(s, ast.Constant) and isinstance(s.value, int):
                    subscript_index_assigns.append(s.value)
                elif isinstance(s, ast.Index) and isinstance(getattr(s, "value", None), ast.Constant):
                    v = s.value.value
                    if isinstance(v, int):
                        subscript_index_assigns.append(v)
    forbidden = {2, 3}
    used_forbidden = any(i in forbidden for i in subscript_index_assigns)
    assert used_forbidden is False, f"expected={False!r} actual={used_forbidden!r}"


def test_slice_assignment_targets_correct_range_and_values():
    src = inspect.getsource(mod)
    tree = ast.parse(src)

    found = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for t in node.targets:
            if not (isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Slice)):
                continue
            # target should be data[2:4] (or equivalent with omitted end/start forms)
            sl = t.slice
            start = sl.lower.value if isinstance(sl.lower, ast.Constant) else None
            stop = sl.upper.value if isinstance(sl.upper, ast.Constant) else None

            # value should be [7, 8]
            if isinstance(node.value, (ast.List, ast.Tuple)):
                elts = node.value.elts
                if len(elts) == 2 and all(isinstance(e, ast.Constant) for e in elts):
                    vals = [e.value for e in elts]
                else:
                    vals = None
            else:
                vals = None

            if start == 2 and stop == 4 and vals == [7, 8]:
                found = True
                break
        if found:
            break

    assert found is True, f"expected={True!r} actual={found!r}"


def test_no_hardcoded_print_of_expected_literal():
    src = inspect.getsource(mod)
    # Disallow printing the literal list directly rather than printing data
    hardcoded = bool(re.search(r"print\(\s*\[\s*1\s*,\s*2\s*,\s*7\s*,\s*8\s*,\s*5\s*\]\s*\)", src))
    assert hardcoded is False, f"expected={False!r} actual={hardcoded!r}"