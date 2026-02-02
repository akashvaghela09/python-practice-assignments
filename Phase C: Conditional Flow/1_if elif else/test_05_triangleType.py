import importlib.util
import os
import sys


def load_module():
    filename = "05_triangleType.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("triangle_mod_05", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def run_with_sides(a, b, c):
    mod = load_module()
    mod.a, mod.b, mod.c = a, b, c

    out = []

    def fake_print(*args, **kwargs):
        out.append(" ".join(str(x) for x in args))

    mod.print = fake_print
    if hasattr(mod, "__dict__"):
        exec(compile(open(mod.__file__, "r", encoding="utf-8").read(), mod.__file__, "exec"), mod.__dict__)

    return "\n".join(out).strip()


def expected_type(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle"
    if a + b <= c or a + c <= b or b + c <= a:
        return "Not a triangle"
    if a == b == c:
        return "Equilateral"
    if a == b or a == c or b == c:
        return "Isosceles"
    return "Scalene"


def assert_output_matches(a, b, c):
    expected = expected_type(a, b, c)
    actual = run_with_sides(a, b, c)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_exactly_one_line():
    mod = load_module()
    out = []
    mod.print = lambda *args, **kwargs: out.append(" ".join(str(x) for x in args))
    exec(compile(open(mod.__file__, "r", encoding="utf-8").read(), mod.__file__, "exec"), mod.__dict__)
    joined = "\n".join(out).strip()
    assert joined.count("\n") == 0, f"expected={0!r} actual={joined.count(chr(10))!r}"
    assert joined != "", f"expected={'non-empty'!r} actual={joined!r}"


def test_default_values_from_assignment():
    assert_output_matches(2, 2, 3)


def test_not_a_triangle_non_positive_side():
    assert_output_matches(0, 2, 3)
    assert_output_matches(-1, 2, 2)
    assert_output_matches(3, 0, 3)


def test_not_a_triangle_triangle_inequality_failures():
    assert_output_matches(1, 2, 3)
    assert_output_matches(2, 3, 1)
    assert_output_matches(3, 1, 2)
    assert_output_matches(5, 1, 1)


def test_equilateral():
    assert_output_matches(4, 4, 4)
    assert_output_matches(1, 1, 1)


def test_isosceles_variants():
    assert_output_matches(5, 5, 8)
    assert_output_matches(5, 8, 5)
    assert_output_matches(8, 5, 5)


def test_scalene():
    assert_output_matches(4, 5, 6)
    assert_output_matches(7, 8, 9)


def test_output_is_one_of_allowed_strings():
    mod = load_module()
    out = []
    mod.print = lambda *args, **kwargs: out.append(" ".join(str(x) for x in args))
    exec(compile(open(mod.__file__, "r", encoding="utf-8").read(), mod.__file__, "exec"), mod.__dict__)
    actual = "\n".join(out).strip()
    allowed = {"Not a triangle", "Equilateral", "Isosceles", "Scalene"}
    assert actual in allowed, f"expected={sorted(allowed)!r} actual={actual!r}"