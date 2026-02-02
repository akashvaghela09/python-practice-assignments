import importlib.util
import pathlib
import re


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "07_eventEntryPolicy.py"
    spec = importlib.util.spec_from_file_location("event_entry_policy_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _extract_values(stdout_text):
    m = re.search(
        r"expected\s*vs\s*actual\s*:\s*(?P<expected>ENTER|DENY)\s*vs\s*(?P<actual>ENTER|DENY)",
        stdout_text,
        flags=re.IGNORECASE,
    )
    if not m:
        return None, None
    return m.group("expected").upper(), m.group("actual").upper()


def test_prints_exactly_enter_or_deny_only(capsys):
    _load_module()
    out = capsys.readouterr().out
    tokens = re.findall(r"\S+", out)
    assert len(tokens) == 1, "expected vs actual: 1 token vs %s tokens" % (len(tokens))
    assert tokens[0] in ("ENTER", "DENY"), "expected vs actual: ENTER/DENY vs %s" % (tokens[0],)


def test_default_scenario_matches_policy(capsys):
    mod = _load_module()
    out = capsys.readouterr().out.strip()
    has_ticket = getattr(mod, "has_ticket")
    is_vip = getattr(mod, "is_vip")
    on_guest_list = getattr(mod, "on_guest_list")
    age = getattr(mod, "age")
    accompanied = getattr(mod, "accompanied")

    regular_entry = bool(has_ticket) and (age >= 18 or bool(accompanied))
    vip_entry = bool(is_vip) and bool(on_guest_list)
    expected = "ENTER" if (regular_entry or vip_entry) else "DENY"

    assert out in ("ENTER", "DENY"), "expected vs actual: ENTER/DENY vs %s" % (out,)
    assert out == expected, "expected vs actual: %s vs %s" % (expected, out)


def test_alternate_scenario_from_prompt_policy_logic_only(capsys):
    mod = _load_module()
    capsys.readouterr()

    has_ticket = True
    is_vip = False
    on_guest_list = False
    age = 16
    accompanied = False

    regular_entry = bool(has_ticket) and (age >= 18 or bool(accompanied))
    vip_entry = bool(is_vip) and bool(on_guest_list)
    expected = "ENTER" if (regular_entry or vip_entry) else "DENY"

    actual = "ENTER" if (regular_entry or vip_entry) else "DENY"

    assert actual == expected, "expected vs actual: %s vs %s" % (expected, actual)


def test_policy_truth_table_minimal_cases(capsys):
    _load_module()
    capsys.readouterr()

    cases = [
        # (has_ticket, is_vip, on_guest_list, age, accompanied)
        (False, True, True, 10, False),
        (False, True, False, 30, False),
        (True, False, False, 17, True),
        (True, False, False, 17, False),
        (True, False, False, 18, False),
        (False, False, False, 25, False),
    ]
    for has_ticket, is_vip, on_guest_list, age, accompanied in cases:
        regular_entry = bool(has_ticket) and (age >= 18 or bool(accompanied))
        vip_entry = bool(is_vip) and bool(on_guest_list)
        expected = "ENTER" if (regular_entry or vip_entry) else "DENY"
        actual = "ENTER" if (regular_entry or vip_entry) else "DENY"
        assert actual == expected, "expected vs actual: %s vs %s" % (expected, actual)


def test_has_required_variables_defined():
    mod = _load_module()
    for name in ("has_ticket", "is_vip", "on_guest_list", "age", "accompanied"):
        assert hasattr(mod, name), "expected vs actual: attribute present vs missing"

    assert isinstance(getattr(mod, "age"), int), "expected vs actual: int vs %s" % (type(getattr(mod, "age")).__name__,)