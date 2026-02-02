import importlib.util
import io
import os
import contextlib
import pathlib
import re
import ast


def _load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("mod09_membershipAndComparisonChain", path)
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_prints_true_only():
    path = pathlib.Path(__file__).resolve().parent / "09_membershipAndComparisonChain.py"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(str(path))
    out = buf.getvalue()
    assert out == "True\n", f"expected={repr('True\\n')} actual={repr(out)}"


def test_result_is_true_and_types():
    path = pathlib.Path(__file__).resolve().parent / "09_membershipAndComparisonChain.py"
    m = _load_module_from_path(str(path))
    assert isinstance(m.result, bool), f"expected={bool} actual={type(m.result)}"
    assert m.result is True, f"expected={True} actual={m.result}"
    assert isinstance(m.nums, list), f"expected={list} actual={type(m.nums)}"
    assert len(m.nums) == 4, f"expected={4} actual={len(m.nums)}"


def test_expression_components_hold():
    path = pathlib.Path(__file__).resolve().parent / "09_membershipAndComparisonChain.py"
    m = _load_module_from_path(str(path))

    assert (1 < m.x) is True, f"expected={True} actual={(1 < m.x)}"
    assert (m.x <= 3) is True, f"expected={True} actual={(m.x <= 3)}"
    assert (m.x in m.nums) is True, f"expected={True} actual={(m.x in m.nums)}"

    recomputed = (1 < m.x <= 3) and (m.x in m.nums)
    assert recomputed is True, f"expected={True} actual={recomputed}"
    assert recomputed == m.result, f"expected={recomputed} actual={m.result}"


def test_source_has_required_expression_structure():
    path = pathlib.Path(__file__).resolve().parent / "09_membershipAndComparisonChain.py"
    src = path.read_text(encoding="utf-8")

    tree = ast.parse(src, filename=str(path))
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    result_assign = None
    for a in assigns:
        for t in a.targets:
            if isinstance(t, ast.Name) and t.id == "result":
                result_assign = a
                break
        if result_assign:
            break

    assert result_assign is not None, f"expected={'result assignment'} actual={None}"

    val = result_assign.value
    assert isinstance(val, ast.BoolOp) and isinstance(val.op, ast.And), f"expected={ast.And} actual={type(getattr(val, 'op', None))}"

    assert len(val.values) == 2, f"expected={2} actual={len(getattr(val, 'values', []))}"

    left, right = val.values
    assert isinstance(left, ast.Compare), f"expected={ast.Compare} actual={type(left)}"
    assert isinstance(right, ast.Compare), f"expected={ast.Compare} actual={type(right)}"

    assert isinstance(left.left, ast.Constant) and left.left.value == 1, f"expected={1} actual={getattr(left.left, 'value', None)}"
    assert len(left.ops) == 2 and isinstance(left.ops[0], ast.Lt) and isinstance(left.ops[1], ast.LtE), f"expected={('Lt','LtE')} actual={tuple(type(o).__name__ for o in getattr(left, 'ops', []))}"

    assert len(left.comparators) == 2, f"expected={2} actual={len(getattr(left, 'comparators', []))}"
    assert isinstance(left.comparators[0], ast.Name) and left.comparators[0].id == "x", f"expected={'x'} actual={getattr(left.comparators[0], 'id', None)}"
    assert isinstance(left.comparators[1], ast.Constant) and left.comparators[1].value == 3, f"expected={3} actual={getattr(left.comparators[1], 'value', None)}"

    assert isinstance(right.left, ast.Name) and right.left.id == "x", f"expected={'x'} actual={getattr(right.left, 'id', None)}"
    assert len(right.ops) == 1 and isinstance(right.ops[0], ast.In), f"expected={'In'} actual={tuple(type(o).__name__ for o in getattr(right, 'ops', []))}"
    assert len(right.comparators) == 1 and isinstance(right.comparators[0], ast.Name) and right.comparators[0].id == "nums", f"expected={'nums'} actual={getattr(right.comparators[0], 'id', None)}"


def test_no_placeholders_remain():
    path = pathlib.Path(__file__).resolve().parent / "09_membershipAndComparisonChain.py"
    src = path.read_text(encoding="utf-8")
    placeholders = re.findall(r"\b__\b", src)
    assert len(placeholders) == 0, f"expected={0} actual={len(placeholders)}"