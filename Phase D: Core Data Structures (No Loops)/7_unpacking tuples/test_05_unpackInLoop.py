import importlib.util
import os
import sys
import re
import ast
import pytest


ASSIGNMENT_FILE = "05_unpackInLoop.py"


def load_module_capture_stdout(path):
    spec = importlib.util.spec_from_file_location("student_mod_05_unpackInLoop", path)
    mod = importlib.util.module_from_spec(spec)
    old_stdout = sys.stdout
    try:
        from io import StringIO

        buf = StringIO()
        sys.stdout = buf
        spec.loader.exec_module(mod)
        return mod, buf.getvalue()
    finally:
        sys.stdout = old_stdout


def compute_expected(points):
    return "\n".join([f"x={x}, y={y}" for x, y in points])


def parse_points_from_source(source):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "points":
                    return ast.literal_eval(node.value)
    raise AssertionError("Unable to locate points assignment in source")


def normalize_output(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in s.strip().split("\n")] if s.strip() else []
    return "\n".join(lines)


def test_output_matches_expected_from_points():
    assert os.path.exists(ASSIGNMENT_FILE)
    with open(ASSIGNMENT_FILE, "r", encoding="utf-8") as f:
        source = f.read()

    points = parse_points_from_source(source)
    expected = compute_expected(points)

    mod, printed = load_module_capture_stdout(ASSIGNMENT_FILE)

    actual = getattr(mod, "output", None)
    assert actual is not None
    assert normalize_output(actual) == normalize_output(expected), f"expected={normalize_output(expected)!r} actual={normalize_output(actual)!r}"
    assert normalize_output(printed) == normalize_output(expected), f"expected={normalize_output(expected)!r} actual={normalize_output(printed)!r}"


def test_result_lines_structure_and_contents():
    mod, _ = load_module_capture_stdout(ASSIGNMENT_FILE)

    assert hasattr(mod, "points")
    assert hasattr(mod, "result_lines")
    assert isinstance(mod.result_lines, list)

    expected_lines = [f"x={x}, y={y}" for x, y in mod.points]
    assert len(mod.result_lines) == len(expected_lines), f"expected={len(expected_lines)!r} actual={len(mod.result_lines)!r}"

    for exp, act in zip(expected_lines, mod.result_lines):
        assert act == exp, f"expected={exp!r} actual={act!r}"


def test_uses_tuple_unpacking_in_loop():
    with open(ASSIGNMENT_FILE, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    for_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
    assert for_nodes, f"expected={True!r} actual={False!r}"

    found_unpack_over_points = False
    for n in for_nodes:
        is_over_points = isinstance(n.iter, ast.Name) and n.iter.id == "points"
        is_unpack = isinstance(n.target, (ast.Tuple, ast.List)) and len(n.target.elts) == 2
        if is_over_points and is_unpack:
            found_unpack_over_points = True
            break

    assert found_unpack_over_points, f"expected={True!r} actual={found_unpack_over_points!r}"


def test_format_exactness_no_extra_spaces():
    mod, _ = load_module_capture_stdout(ASSIGNMENT_FILE)
    out = normalize_output(mod.output)
    lines = out.split("\n") if out else []
    assert len(lines) == len(mod.points), f"expected={len(mod.points)!r} actual={len(lines)!r}"

    pattern = re.compile(r"^x=\-?\d+, y=\-?\d+$")
    checks = [bool(pattern.match(line)) for line in lines]
    assert all(checks), f"expected={True!r} actual={all(checks)!r}"