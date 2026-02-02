import importlib.util
import pathlib
import re
import ast
import pytest


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _repo_file_path():
    return pathlib.Path(__file__).resolve().parent / "14_setComprehensionSquares.py"


def _extract_printed_repr(output: str) -> str:
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    if not lines:
        return ""
    return lines[-1]


def test_source_has_set_comprehension_not_set_call():
    path = _repo_file_path()
    src = path.read_text(encoding="utf-8")
    assert "____" not in src, "expected vs actual: placeholder present vs placeholder absent"

    tree = ast.parse(src)
    setcomp_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.SetComp)]
    assert len(setcomp_nodes) >= 1, "expected vs actual: setcomp found vs setcomp missing"

    set_call = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "set":
            set_call = True
            break
    assert not set_call, "expected vs actual: no set() call vs set() call detected"


def test_module_prints_expected_set(capsys):
    path = _repo_file_path()
    module = _load_module_from_path(path)
    captured = capsys.readouterr()
    printed = _extract_printed_repr(captured.out)

    expected_set = {0, 1, 4, 9, 16}
    try:
        actual = ast.literal_eval(printed)
    except Exception:
        pytest.fail("expected vs actual: printed set literal vs non-literal/invalid output")

    assert isinstance(actual, set), "expected vs actual: type set vs non-set"
    assert actual == expected_set, f"expected vs actual: {expected_set!r} vs {actual!r}"

    assert hasattr(module, "squares"), "expected vs actual: squares exists vs squares missing"
    assert isinstance(module.squares, set), "expected vs actual: module.squares set vs non-set"
    assert module.squares == expected_set, f"expected vs actual: {expected_set!r} vs {module.squares!r}"


def test_squares_uses_nums_and_expression_is_square():
    path = _repo_file_path()
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)

    assign_nodes = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "squares" for t in n.targets)
    ]
    assert assign_nodes, "expected vs actual: squares assignment exists vs missing"
    value = assign_nodes[0].value
    assert isinstance(value, ast.SetComp), "expected vs actual: set comprehension vs not set comprehension"

    gens = value.generators
    assert len(gens) >= 1, "expected vs actual: generator present vs missing"
    gen0 = gens[0]
    assert isinstance(gen0.iter, ast.Name) and gen0.iter.id == "nums", "expected vs actual: iter nums vs different iter"

    elt = value.elt
    is_square = False
    if isinstance(elt, ast.BinOp) and isinstance(elt.op, ast.Mult):
        left, right = elt.left, elt.right
        if isinstance(left, ast.Name) and isinstance(right, ast.Name) and left.id == right.id:
            is_square = True
    assert is_square, "expected vs actual: n*n pattern vs different expression"