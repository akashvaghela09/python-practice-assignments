import ast
import importlib.util
import io
import pathlib
import contextlib

FILE_NAME = "02_updateAndAdd.py"


def load_module():
    path = pathlib.Path(FILE_NAME)
    spec = importlib.util.spec_from_file_location("mod_02_updateAndAdd", str(path))
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


def test_printed_profile_matches_expected_dict():
    module, out = load_module()
    printed = out.strip()
    expected = {"status": "active", "points": 15}
    assert ast.literal_eval(printed) == expected


def test_profile_variable_updated_in_module():
    module, _ = load_module()
    expected = {"status": "active", "points": 15}
    assert getattr(module, "profile", None) == expected


def test_profile_contains_only_expected_keys():
    module, _ = load_module()
    profile = getattr(module, "profile", None)
    assert isinstance(profile, dict)
    assert set(profile.keys()) == {"status", "points"}