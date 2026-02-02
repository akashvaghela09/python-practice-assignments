import importlib.util
import pathlib
import sys


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "04_loginCheck.py"
    spec = importlib.util.spec_from_file_location("loginCheck04", str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["loginCheck04"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_module_executes_without_syntax_error():
    _load_module()


def test_default_variables_exist_and_types():
    mod = _load_module()
    assert hasattr(mod, "username")
    assert hasattr(mod, "password")
    assert hasattr(mod, "expected_password")
    assert hasattr(mod, "has_reset_token")
    assert isinstance(mod.username, str)
    assert isinstance(mod.password, str)
    assert isinstance(mod.expected_password, str)
    assert isinstance(mod.has_reset_token, bool)