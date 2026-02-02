import importlib
import sys
import types
import pytest


MODULE_NAME = "06_booleanInIf"


def load_module(capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    try:
        mod = importlib.import_module(MODULE_NAME)
    except Exception as e:
        pytest.fail(f"expected=module_import_success actual={type(e).__name__}: {e}")
    out = capsys.readouterr().out
    return mod, out


def test_prints_exactly_one_line(capsys):
    _, out = load_module(capsys)
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected=1_line actual={len(lines)}"


def test_output_is_expected_branch_for_false(capsys):
    mod, out = load_module(capsys)
    expected = "Member price" if getattr(mod, "is_member", None) else "Regular price"
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_has_no_extra_whitespace(capsys):
    _, out = load_module(capsys)
    actual = out
    assert actual.endswith("\n"), f"expected=endswith_newline actual={actual!r}"
    assert actual.strip() == actual[:-1], f"expected=stripped_equals_line actual={actual!r}"


def test_is_member_defined_and_boolean(capsys):
    mod, _ = load_module(capsys)
    assert hasattr(mod, "is_member"), "expected=is_member_defined actual=missing"
    assert isinstance(mod.is_member, bool), f"expected=bool actual={type(mod.is_member).__name__}"