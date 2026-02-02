import ast
import importlib.util
import io
import os
import sys


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_placeholders_and_valid_syntax():
    file_path = os.path.join(os.path.dirname(__file__), "01_printZeroToFour.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    assert "____" not in src, f"expected no placeholders, actual placeholders found in source"

    try:
        ast.parse(src)
    except SyntaxError as e:
        assert False, f"expected valid python syntax, actual SyntaxError: {e}"


def test_prints_0_to_4_each_on_own_line():
    file_path = os.path.join(os.path.dirname(__file__), "01_printZeroToFour.py")

    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        _load_module("printZeroToFour_student", file_path)
    finally:
        sys.stdout = old_stdout

    actual = buf.getvalue()
    expected = "0\n1\n2\n3\n4\n"
    assert actual == expected, f"expected:\n{expected!r}\nactual:\n{actual!r}"


def test_uses_for_loop_with_range():
    file_path = os.path.join(os.path.dirname(__file__), "01_printZeroToFour.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert len(for_nodes) == 1, f"expected 1 for-loop, actual {len(for_nodes)}"

    target_for = for_nodes[0]
    assert isinstance(target_for.iter, ast.Call), f"expected range(...) call, actual {ast.dump(target_for.iter)}"
    assert isinstance(target_for.iter.func, ast.Name) and target_for.iter.func.id == "range", (
        f"expected iter to be range(...), actual {ast.dump(target_for.iter)}"
    )

    print_calls = [
        n for n in ast.walk(target_for)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
    ]
    assert len(print_calls) >= 1, f"expected at least 1 print call in loop, actual {len(print_calls)}"