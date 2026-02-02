import importlib
import ast
import pytest

MODULE_NAME = "03_aliasingSameList"


def _run_main_and_capture(capsys):
    mod = importlib.import_module(MODULE_NAME)
    mod.main()
    out = capsys.readouterr().out
    return out


def test_output_exact(capsys):
    out = _run_main_and_capture(capsys)
    expected = 'a: ["x", "y", "z"]\n' + 'b: ["x", "y", "z"]\n'
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_no_extra_output(capsys):
    out = _run_main_and_capture(capsys)
    expected_lines = ['a: ["x", "y", "z"]', 'b: ["x", "y", "z"]']
    actual_lines = [line for line in out.splitlines() if line.strip() != ""]
    assert expected_lines == actual_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_aliasing_present_in_source():
    mod = importlib.import_module(MODULE_NAME)
    src = getattr(mod, "__file__", None)
    assert src is not None
    with open(src, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)

    main_func = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            main_func = node
            break
    assert main_func is not None

    assigned_a = False
    b_aliases_a = False
    mutation_via_b = False

    for node in ast.walk(main_func):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "a":
                    assigned_a = True
                if isinstance(tgt, ast.Name) and tgt.id == "b":
                    if isinstance(node.value, ast.Name) and node.value.id == "a":
                        b_aliases_a = True

        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id == "b":
                if fn.attr in {"append", "extend", "insert"}:
                    mutation_via_b = True

        if isinstance(node, ast.Subscript):
            val = node.value
            if isinstance(val, ast.Name) and val.id == "b":
                parent = node
                # look for assignment to b[...]
                # handled by scanning Assign nodes separately below

    for node in ast.walk(main_func):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Subscript) and isinstance(tgt.value, ast.Name) and tgt.value.id == "b":
                    mutation_via_b = True
        if isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Subscript) and isinstance(node.target.value, ast.Name) and node.target.value.id == "b":
                mutation_via_b = True
            if isinstance(node.target, ast.Name) and node.target.id == "b":
                mutation_via_b = True

    assert (assigned_a and b_aliases_a and mutation_via_b) is True, (
        f"expected={(True, True, True)!r} actual={(assigned_a, b_aliases_a, mutation_via_b)!r}"
    )