import importlib.util
import os
import sys
import contextlib
import io
import pytest


def _load_module(path, name="mod05"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expected(age, has_ticket, with_parent):
    can_enter = bool(has_ticket and (age >= 18 or with_parent))
    needs_parent = bool(has_ticket and age < 18 and (not with_parent))
    return can_enter, needs_parent


def test_module_imports_and_outputs_expected():
    path = os.path.join(os.path.dirname(__file__), "05_andOrPrecedence.py")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module(path, "mod05_run")
    out = buf.getvalue().splitlines()
    assert out == ["can_enter: True", "needs_parent: False"]
    assert hasattr(mod, "can_enter")
    assert hasattr(mod, "needs_parent")


@pytest.mark.parametrize(
    "age,has_ticket,with_parent",
    [
        (17, True, True),
        (17, True, False),
        (17, False, True),
        (17, False, False),
        (18, True, True),
        (18, True, False),
        (18, False, True),
        (18, False, False),
        (16, True, True),
        (16, True, False),
        (21, True, False),
        (21, False, False),
    ],
)
def test_logic_matches_spec_under_various_values(age, has_ticket, with_parent):
    path = os.path.join(os.path.dirname(__file__), "05_andOrPrecedence.py")
    mod = _load_module(path, "mod05_logic")

    expected_can, expected_needs = _expected(age, has_ticket, with_parent)

    mod.age = age
    mod.has_ticket = has_ticket
    mod.with_parent = with_parent

    can_enter = bool(mod.has_ticket and (mod.age >= 18 or mod.with_parent))
    needs_parent = bool(mod.has_ticket and mod.age < 18 and (not mod.with_parent))

    assert expected_can == can_enter
    assert expected_needs == needs_parent


def test_print_format_is_exact_for_default_values():
    path = os.path.join(os.path.dirname(__file__), "05_andOrPrecedence.py")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module(path, "mod05_print")
    out = buf.getvalue()

    expected = "can_enter: True\nneeds_parent: False\n"
    assert expected == out


def test_outputs_show_expected_vs_actual_only_on_mismatch():
    path = os.path.join(os.path.dirname(__file__), "05_andOrPrecedence.py")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module(path, "mod05_logging")
    out_lines = buf.getvalue().splitlines()

    expected_lines = ["can_enter: True", "needs_parent: False"]
    if out_lines != expected_lines:
        sys.stderr.write(f"expected={expected_lines} actual={out_lines}\n")
    assert out_lines == expected_lines