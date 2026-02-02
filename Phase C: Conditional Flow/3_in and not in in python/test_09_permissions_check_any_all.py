import importlib
import ast
import io
import contextlib


def run_module_capture(module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_output_exact_missing_delete():
    out = run_module_capture("09_permissions_check_any_all")
    expected = "missing: ['delete']\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_missing_variable_is_correct_list():
    mod = importlib.import_module("09_permissions_check_any_all")
    expected = ["delete"]
    actual = getattr(mod, "missing", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_extra_output_lines():
    out = run_module_capture("09_permissions_check_any_all")
    expected_lines = ["missing: ['delete']"]
    actual_lines = [line for line in out.splitlines() if line.strip() != ""]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_source_uses_in_for_membership_check():
    mod = importlib.import_module("09_permissions_check_any_all")
    with open(mod.__file__, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    in_ops = [n for n in ast.walk(tree) if isinstance(n, ast.Compare) and any(isinstance(op, ast.In) for op in n.ops)]
    not_in_ops = [
        n for n in ast.walk(tree) if isinstance(n, ast.Compare) and any(isinstance(op, ast.NotIn) for op in n.ops)
    ]

    actual = (len(in_ops) + len(not_in_ops)) > 0
    expected = True
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_source_mentions_any_or_all():
    mod = importlib.import_module("09_permissions_check_any_all")
    with open(mod.__file__, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    any_calls = [
        n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "any"
    ]
    all_calls = [
        n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "all"
    ]

    actual = (len(any_calls) + len(all_calls)) > 0
    expected = True
    assert actual == expected, f"expected={expected!r} actual={actual!r}"