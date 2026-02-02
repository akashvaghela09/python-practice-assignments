import importlib.util
import pathlib
import sys
import pytest


def load_module_from_path(path: pathlib.Path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_module_imports_and_has_can_reset():
    path = pathlib.Path(__file__).resolve().parent / "07_booleanExpressionWithParentheses.py"
    try:
        mod = load_module_from_path(path)
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")
    except Exception as e:
        pytest.fail(f"expected=import_success actual={type(e).__name__}")
    assert hasattr(mod, "can_reset"), f"expected=attribute_can_reset actual={dir(mod)}"


def test_can_reset_value_matches_rule():
    path = pathlib.Path(__file__).resolve().parent / "07_booleanExpressionWithParentheses.py"
    try:
        mod = load_module_from_path(path)
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")
    except Exception as e:
        pytest.fail(f"expected=import_success actual={type(e).__name__}")

    expected = (mod.email_access or mod.phone_access) and (not mod.account_locked)
    actual = mod.can_reset
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_can_reset_is_boolean_type():
    path = pathlib.Path(__file__).resolve().parent / "07_booleanExpressionWithParentheses.py"
    try:
        mod = load_module_from_path(path)
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")
    except Exception as e:
        pytest.fail(f"expected=import_success actual={type(e).__name__}")

    actual = mod.can_reset
    expected_type = bool
    assert isinstance(actual, expected_type), f"expected={expected_type.__name__} actual={type(actual).__name__}"