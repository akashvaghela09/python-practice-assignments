import importlib.util
import io
import os
import re
import ast
import pytest

MODULE_FILENAME = "08_listComprehensionFilter.py"


def _load_module(tmp_path, source_text):
    p = tmp_path / MODULE_FILENAME
    p.write_text(source_text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_mod", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_syntax_valid():
    here = os.path.dirname(__file__)
    path = os.path.join(here, MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    compile(src, MODULE_FILENAME, "exec")


def test_result_value_and_print(capsys):
    here = os.path.dirname(__file__)
    path = os.path.join(here, MODULE_FILENAME)
    spec = importlib.util.spec_from_file_location("student_mod_run", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out = capsys.readouterr().out.strip()
    assert hasattr(mod, "result")
    assert mod.result == [4, 16], f"expected={[4,16]} actual={mod.result}"
    assert out == "result=[4, 16]", f"expected={'result=[4, 16]'} actual={out}"


def test_uses_list_comprehension_and_filters_evens(tmp_path):
    here = os.path.dirname(__file__)
    path = os.path.join(here, MODULE_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    target_assign = None
    for a in assigns:
        if any(isinstance(t, ast.Name) and t.id == "result" for t in a.targets):
            target_assign = a
            break
    assert target_assign is not None

    assert isinstance(target_assign.value, ast.ListComp), "expected=listcomp actual=not_listcomp"

    lc = target_assign.value
    assert any(isinstance(gen, ast.comprehension) and gen.ifs for gen in lc.generators), "expected=has_if actual=no_if"

    gen = lc.generators[0]
    assert isinstance(gen.iter, ast.Name) and gen.iter.id == "nums", "expected=iter_nums actual=other"

    elt = lc.elt
    assert isinstance(elt, ast.BinOp) and isinstance(elt.op, ast.Mult), "expected=mul actual=not_mul"
    assert isinstance(elt.left, ast.Name) and isinstance(elt.right, ast.Name), "expected=name_name actual=other"
    assert elt.left.id == elt.right.id, "expected=same_name actual=different"

    temp_name = elt.left.id
    if_exprs = gen.ifs
    found_even_check = False
    for ife in if_exprs:
        if isinstance(ife, ast.Compare) and len(ife.ops) == 1 and len(ife.comparators) == 1:
            op = ife.ops[0]
            comp = ife.comparators[0]
            left = ife.left
            if (
                isinstance(op, ast.Eq)
                and isinstance(comp, ast.Constant)
                and comp.value == 0
                and isinstance(left, ast.BinOp)
                and isinstance(left.op, ast.Mod)
                and isinstance(left.left, ast.Name)
                and left.left.id == temp_name
                and isinstance(left.right, ast.Constant)
                and left.right.value == 2
            ):
                found_even_check = True
                break
    assert found_even_check, "expected=even_filter actual=missing"

    mutated = re.sub(r"nums\s*=\s*\[[^\]]*\]", "nums = [0, 5, 6, -2, 7]", src, count=1)
    _load_module(tmp_path, mutated)
    cap = io.StringIO()
    spec = importlib.util.spec_from_file_location("student_mod_mut", str(tmp_path / MODULE_FILENAME))
    mod2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod2)
    assert mod2.result == [0, 36, 4], f"expected={[0,36,4]} actual={mod2.result}"