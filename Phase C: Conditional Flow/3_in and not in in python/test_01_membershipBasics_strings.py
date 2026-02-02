import runpy
import io
import contextlib
import ast
import importlib.util
import pathlib
import sys


FILE = "01_membershipBasics_strings.py"


def _run_script_capture():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(FILE, run_name="__main__")
    return buf.getvalue()


def test_output_lines_exact():
    out = _run_script_capture()
    lines = [line.rstrip("\n") for line in out.splitlines()]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    assert lines[0] == "True", f"expected={'True'!r} actual={lines[0]!r}"
    assert lines[1] == "False", f"expected={'False'!r} actual={lines[1]!r}"


def test_no_none_printed():
    out = _run_script_capture()
    assert "None" not in out, f"expected={False!r} actual={('None' in out)!r}"


def test_source_uses_in_operator_twice():
    p = pathlib.Path(FILE)
    src = p.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=FILE)

    compares = [n for n in ast.walk(tree) if isinstance(n, ast.Compare)]
    in_ops = 0
    for c in compares:
        in_ops += sum(1 for op in c.ops if isinstance(op, ast.In))

    assert in_ops >= 2, f"expected={2!r} actual={in_ops!r}"


def test_source_does_not_print_none_literal():
    p = pathlib.Path(FILE)
    src = p.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=FILE)

    bad_prints = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and arg.value is None:
                    bad_prints += 1

    assert bad_prints == 0, f"expected={0!r} actual={bad_prints!r}"


def test_module_importable():
    spec = importlib.util.spec_from_file_location("assignment_mod", FILE)
    module = importlib.util.module_from_spec(spec)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        spec.loader.exec_module(module)
    out = stdout.getvalue().splitlines()
    assert len(out) == 2, f"expected={2!r} actual={len(out)!r}"