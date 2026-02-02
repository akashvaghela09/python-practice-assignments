import importlib.util
import io
import os
import contextlib

MODULE_FILE = "02_fullNameConcat.py"


def load_module():
    spec = importlib.util.spec_from_file_location("mod_02_fullNameConcat", MODULE_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        module = load_module()
    return module, buf.getvalue()


def test_full_variable_is_correct_string():
    module = load_module()
    expected = f"{module.first} {module.last}"
    assert module.full == expected, f"expected={expected!r} actual={module.full!r}"


def test_printed_output_matches_full_name_line():
    module, out = capture_stdout()
    expected = f"{module.first} {module.last}\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_full_is_string_type():
    module = load_module()
    expected = str
    actual = type(module.full)
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_no_leading_or_trailing_whitespace_in_full():
    module = load_module()
    expected = module.full
    actual = module.full.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_full_contains_exactly_one_space_between_names():
    module = load_module()
    expected = 1
    actual = module.full.count(" ")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_source_does_not_leave_full_as_none():
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    expected = False
    actual = "full = None" in content
    assert actual == expected, f"expected={expected!r} actual={actual!r}"