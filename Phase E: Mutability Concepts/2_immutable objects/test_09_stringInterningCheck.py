import importlib.util
import os
import sys


def _load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("mod_09_stringInterningCheck", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_output_equal_and_identical(capsys):
    _load_module_from_filename("09_stringInterningCheck.py")
    out = capsys.readouterr().out.strip().splitlines()

    expected = ["equal: True", "identical: False"]
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_are_defined_and_correct_types():
    mod = _load_module_from_filename("09_stringInterningCheck.py")
    assert hasattr(mod, "a"), "expected='a' actual=missing"
    assert hasattr(mod, "b"), "expected='b' actual=missing"
    assert isinstance(mod.a, str), f"expected={str!r} actual={type(mod.a)!r}"
    assert isinstance(mod.b, str), f"expected={str!r} actual={type(mod.b)!r}"


def test_equality_and_identity_semantics():
    mod = _load_module_from_filename("09_stringInterningCheck.py")
    eq_actual = (mod.a == mod.b)
    id_actual = (mod.a is mod.b)

    eq_expected = True
    id_expected = False

    assert eq_actual == eq_expected, f"expected={eq_expected!r} actual={eq_actual!r}"
    assert id_actual == id_expected, f"expected={id_expected!r} actual={id_actual!r}"


def test_a_is_literal_python_and_b_equals_python():
    mod = _load_module_from_filename("09_stringInterningCheck.py")

    expected_a = "python"
    expected_b = "python"

    assert mod.a == expected_a, f"expected={expected_a!r} actual={mod.a!r}"
    assert mod.b == expected_b, f"expected={expected_b!r} actual={mod.b!r}"


def test_b_is_dynamically_constructed_not_same_object_as_literal_python():
    mod = _load_module_from_filename("09_stringInterningCheck.py")

    literal = "python"
    same_as_literal = (mod.b is literal)
    expected = False

    assert same_as_literal == expected, f"expected={expected!r} actual={same_as_literal!r}"