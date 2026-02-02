import importlib.util
import pathlib


def _load_student_module():
    path = pathlib.Path(__file__).with_name("16_validateRectangularMatrix.py")
    spec = importlib.util.spec_from_file_location("validateRectangularMatrix16", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_is_rect_values():
    mod = _load_student_module()
    expected1, expected2 = True, False
    assert mod.is_rect1 == expected1, f"expected={expected1} actual={mod.is_rect1}"
    assert mod.is_rect2 == expected2, f"expected={expected2} actual={mod.is_rect2}"


def test_printed_output_exact(capsys):
    _load_student_module()
    out = capsys.readouterr().out
    expected = "True False\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_is_rect_types_are_bool():
    mod = _load_student_module()
    expected_type = bool
    assert isinstance(mod.is_rect1, expected_type), f"expected={expected_type} actual={type(mod.is_rect1)}"
    assert isinstance(mod.is_rect2, expected_type), f"expected={expected_type} actual={type(mod.is_rect2)}"