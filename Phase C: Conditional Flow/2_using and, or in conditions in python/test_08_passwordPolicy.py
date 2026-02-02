import importlib.util
import pathlib
import re


def _run_module_capture_stdout(module_path):
    spec = importlib.util.spec_from_file_location("pw_policy_mod", str(module_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_source_has_no_placeholder():
    path = pathlib.Path(__file__).resolve().parent / "08_passwordPolicy.py"
    src = path.read_text(encoding="utf-8")
    assert "____" not in src, f"expected placeholder absent, actual present"


def test_prints_valid_for_default_password(capsys):
    path = pathlib.Path(__file__).resolve().parent / "08_passwordPolicy.py"
    _run_module_capture_stdout(path)
    out = capsys.readouterr().out.strip().splitlines()
    got = out[-1].strip() if out else ""
    exp = "VALID"
    assert got == exp, f"expected {exp}, actual {got}"


def test_condition_matches_spec_for_multiple_passwords(capsys):
    path = pathlib.Path(__file__).resolve().parent / "08_passwordPolicy.py"
    src = path.read_text(encoding="utf-8")

    m = re.search(r'^\s*if\s+(.*?):\s*$', src, flags=re.MULTILINE)
    assert m is not None, "expected condition line, actual missing"
    cond = m.group(1).strip()
    assert "____" not in cond, "expected concrete condition, actual placeholder"

    pre = (
        "def _check(password):\n"
        "    has_digit = any(ch.isdigit() for ch in password)\n"
        "    has_special = any(ch in '!@#' for ch in password)\n"
        "    has_space = (' ' in password)\n"
        f"    return bool({cond})\n"
    )
    ns = {}
    exec(pre, ns, ns)
    check = ns["_check"]

    cases = [
        ("abcde1fg", True),
        ("abcd e1fg", False),
        ("abcdefgh", False),
        ("abcd!efg", True),
        ("abcd@ ef", False),
        ("12345678", True),
        ("!@#abcd", True),
        ("a1 bcd!!", False),
        ("a!b@c#d", False),
        ("        ", False),
    ]

    for pw, exp in cases:
        got = bool(check(pw))
        assert got == exp, f"expected {exp}, actual {got}"