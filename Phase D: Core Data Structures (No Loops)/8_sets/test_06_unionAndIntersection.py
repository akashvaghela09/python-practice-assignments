import ast
import importlib.util
import os
import re
import sys


def _load_module_capture_output(module_filename):
    spec = importlib.util.spec_from_file_location("student_mod_06", module_filename)
    mod = importlib.util.module_from_spec(spec)

    captured = []

    def _fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    import builtins

    real_print = builtins.print
    builtins.print = _fake_print
    try:
        spec.loader.exec_module(mod)
    finally:
        builtins.print = real_print

    return mod, "".join(captured)


def _parse_set_literal(text):
    s = text.strip()
    if s == "set()":
        return set()
    try:
        node = ast.parse(s, mode="eval").body
    except SyntaxError:
        raise ValueError("not a set literal")
    if isinstance(node, ast.Set):
        values = []
        for elt in node.elts:
            if not isinstance(elt, ast.Constant) or not isinstance(elt.value, int):
                raise ValueError("set has non-int elements")
            values.append(elt.value)
        return set(values)
    raise ValueError("not a set literal")


def _extract_line_value(output, prefix):
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    raise AssertionError(f"missing {prefix!r} line; output={output!r}")


def test_runs_and_prints_union_and_intersection(tmp_path):
    module_filename = os.path.join(os.path.dirname(__file__), "06_unionAndIntersection.py")
    mod, out = _load_module_capture_output(module_filename)

    union_text = _extract_line_value(out, "union:")
    inter_text = _extract_line_value(out, "intersection:")

    actual_union = _parse_set_literal(union_text)
    actual_inter = _parse_set_literal(inter_text)

    expected_union = {1, 2, 3, 4, 5, 6}
    expected_inter = {3, 4}

    assert actual_union == expected_union, f"expected={expected_union!r} actual={actual_union!r}"
    assert actual_inter == expected_inter, f"expected={expected_inter!r} actual={actual_inter!r}"

    assert hasattr(mod, "A") and hasattr(mod, "B"), f"expected={'A and B defined'} actual={sorted([n for n in dir(mod) if n in ('A','B')])!r}"
    assert isinstance(mod.A, set), f"expected={set!r} actual={type(mod.A)!r}"
    assert isinstance(mod.B, set), f"expected={set!r} actual={type(mod.B)!r}"
    assert mod.A == {1, 2, 3, 4}, f"expected={{1,2,3,4}} actual={mod.A!r}"
    assert mod.B == {3, 4, 5, 6}, f"expected={{3,4,5,6}} actual={mod.B!r}"


def test_variables_u_and_inter_are_sets_and_correct():
    module_filename = os.path.join(os.path.dirname(__file__), "06_unionAndIntersection.py")
    mod, _ = _load_module_capture_output(module_filename)

    assert hasattr(mod, "u"), f"expected={'u defined'} actual={hasattr(mod, 'u')!r}"
    assert hasattr(mod, "inter"), f"expected={'inter defined'} actual={hasattr(mod, 'inter')!r}"
    assert isinstance(mod.u, set), f"expected={set!r} actual={type(mod.u)!r}"
    assert isinstance(mod.inter, set), f"expected={set!r} actual={type(mod.inter)!r}"

    expected_u = mod.A | mod.B
    expected_inter = mod.A & mod.B

    assert mod.u == expected_u, f"expected={expected_u!r} actual={mod.u!r}"
    assert mod.inter == expected_inter, f"expected={expected_inter!r} actual={mod.inter!r}"


def test_output_has_exact_two_relevant_lines():
    module_filename = os.path.join(os.path.dirname(__file__), "06_unionAndIntersection.py")
    _, out = _load_module_capture_output(module_filename)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    relevant = [ln for ln in lines if ln.startswith("union:") or ln.startswith("intersection:")]
    assert len(relevant) == 2, f"expected={2!r} actual={len(relevant)!r}"
    assert relevant[0].startswith("union:"), f"expected={'union first'} actual={relevant!r}"
    assert relevant[1].startswith("intersection:"), f"expected={'intersection second'} actual={relevant!r}"


def test_output_set_syntax_is_parseable():
    module_filename = os.path.join(os.path.dirname(__file__), "06_unionAndIntersection.py")
    _, out = _load_module_capture_output(module_filename)

    union_text = _extract_line_value(out, "union:")
    inter_text = _extract_line_value(out, "intersection:")

    union_ok = True
    inter_ok = True
    try:
        _parse_set_literal(union_text)
    except Exception:
        union_ok = False
    try:
        _parse_set_literal(inter_text)
    except Exception:
        inter_ok = False

    assert union_ok is True, f"expected={True!r} actual={union_ok!r}"
    assert inter_ok is True, f"expected={True!r} actual={inter_ok!r}"