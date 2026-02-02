import ast
import importlib.util
import io
import os
import sys
import contextlib
import pathlib

FILE_NAME = "04_sortStringsCaseInsensitive.py"


def _load_module(tmp_path):
    src = pathlib.Path(__file__).with_name(FILE_NAME)
    if not src.exists():
        src = pathlib.Path(FILE_NAME)
    assert src.exists()

    dst = tmp_path / FILE_NAME
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod, buf.getvalue()


def test_names_sorted_case_insensitive_in_place(tmp_path):
    mod, _ = _load_module(tmp_path)
    expected = ["alice", "Bob", "carol", "Dave"]
    actual = getattr(mod, "names", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_uses_in_place_sort_not_reassignment(tmp_path):
    src = pathlib.Path(__file__).with_name(FILE_NAME)
    if not src.exists():
        src = pathlib.Path(FILE_NAME)
    code = src.read_text(encoding="utf-8")
    tree = ast.parse(code)

    sort_calls = []
    assigned_targets = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort" and isinstance(node.func.value, ast.Name) and node.func.value.id == "names":
                sort_calls.append(node)
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "names":
                    assigned_targets.append(node)

    # allow initial assignment, but disallow later reassignment replacing list
    reassignments = [a for a in assigned_targets[1:]]
    expected_has_sort = True
    actual_has_sort = len(sort_calls) >= 1
    assert actual_has_sort == expected_has_sort, f"expected={expected_has_sort} actual={actual_has_sort}"

    expected_reassignments = 0
    actual_reassignments = len(reassignments)
    assert actual_reassignments == expected_reassignments, f"expected={expected_reassignments} actual={actual_reassignments}"


def test_sort_is_case_insensitive_via_key(tmp_path):
    src = pathlib.Path(__file__).with_name(FILE_NAME)
    if not src.exists():
        src = pathlib.Path(FILE_NAME)
    code = src.read_text(encoding="utf-8")
    tree = ast.parse(code)

    key_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort" and isinstance(node.func.value, ast.Name) and node.func.value.id == "names":
                for kw in node.keywords or []:
                    if kw.arg == "key":
                        key_found = True
                        break

    expected = True
    actual = key_found
    assert actual == expected, f"expected={expected} actual={actual}"


def test_prints_resulting_list(tmp_path):
    _, out = _load_module(tmp_path)
    expected = True
    actual = "alice" in out and "Bob" in out and "carol" in out and "Dave" in out
    assert actual == expected, f"expected={expected} actual={actual}"