import importlib.util
import os
import re
import pytest

MODULE_FILE = "10_accessControlMatrix.py"


def load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    spec = importlib.util.spec_from_file_location("access_matrix_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_with_overrides(tmp_path, role, has_2fa, is_on_network, has_invite, is_suspended):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    code = open(src_path, "r", encoding="utf-8").read()

    replacements = {
        r'^\s*role\s*=\s*.*$': f'role = {role!r}',
        r'^\s*has_2fa\s*=\s*.*$': f'has_2fa = {has_2fa!r}',
        r'^\s*is_on_network\s*=\s*.*$': f'is_on_network = {is_on_network!r}',
        r'^\s*has_invite\s*=\s*.*$': f'has_invite = {has_invite!r}',
        r'^\s*is_suspended\s*=\s*.*$': f'is_suspended = {is_suspended!r}',
    }
    for pat, rep in replacements.items():
        code, n = re.subn(pat, rep, code, flags=re.MULTILINE)
        assert n >= 1

    mod_path = tmp_path / "acm_run.py"
    mod_path.write_text(code, encoding="utf-8")

    spec = importlib.util.spec_from_file_location("acm_run_mod", str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def last_printed_line(capsys):
    out = capsys.readouterr().out.strip().splitlines()
    return out[-1] if out else ""


def test_module_imports_and_has_expected_names():
    mod = load_module()
    for name in ("role", "has_2fa", "is_on_network", "has_invite", "is_suspended"):
        assert hasattr(mod, name)


def test_default_scenario_is_limited_access(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="staff",
        has_2fa=True,
        is_on_network=False,
        has_invite=False,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "LIMITED ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_staff_on_network_with_2fa_is_full_access(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="staff",
        has_2fa=True,
        is_on_network=True,
        has_invite=False,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "FULL ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_suspended_always_no_access_overrides_admin(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="admin",
        has_2fa=False,
        is_on_network=True,
        has_invite=True,
        is_suspended=True,
    )
    actual = last_printed_line(capsys)
    expected = "NO ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_admin_full_access_when_not_suspended(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="admin",
        has_2fa=False,
        is_on_network=False,
        has_invite=False,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "FULL ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_guest_with_invite_limited_access(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="guest",
        has_2fa=False,
        is_on_network=False,
        has_invite=True,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "LIMITED ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_guest_without_invite_no_access(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="guest",
        has_2fa=True,
        is_on_network=True,
        has_invite=False,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "NO ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_staff_without_2fa_no_access(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="staff",
        has_2fa=False,
        is_on_network=True,
        has_invite=True,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "NO ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_rule_order_staff_full_requires_both_2fa_and_on_network(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="staff",
        has_2fa=True,
        is_on_network=False,
        has_invite=True,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    expected = "LIMITED ACCESS"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_is_one_of_expected_levels(tmp_path, capsys):
    run_with_overrides(
        tmp_path,
        role="other",
        has_2fa=False,
        is_on_network=False,
        has_invite=False,
        is_suspended=False,
    )
    actual = last_printed_line(capsys)
    assert actual in {"NO ACCESS", "LIMITED ACCESS", "FULL ACCESS"}