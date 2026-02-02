import importlib.util
import inspect
import os
import pathlib
import pytest


def _load_module():
    file_path = pathlib.Path(__file__).resolve().parent / "10_signatureValidation.py"
    assert file_path.exists()
    spec = importlib.util.spec_from_file_location("sigval10", str(file_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_running_file_prints_exact_output(capsys):
    _load_module()
    out = capsys.readouterr().out
    expected = "user=ana; role=admin; active=True\nuser=bob; role=member; active=False\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_format_user_return_values_and_ignores_extra_kwargs():
    mod = _load_module()
    res1 = mod.format_user("ana", "admin", active=True, theme="dark", x=1)
    exp1 = "user=ana; role=admin; active=True"
    assert res1 == exp1, f"expected={exp1!r} actual={res1!r}"

    res2 = mod.format_user("bob", active=False, any="thing")
    exp2 = "user=bob; role=member; active=False"
    assert res2 == exp2, f"expected={exp2!r} actual={res2!r}"


def test_signature_enforces_positional_only_and_keyword_only():
    mod = _load_module()
    sig = inspect.signature(mod.format_user)

    params = list(sig.parameters.values())
    assert [p.name for p in params] == ["user", "role", "active", "extra"], f"expected={['user','role','active','extra']!r} actual={[p.name for p in params]!r}"

    kinds = {p.name: p.kind for p in params}
    expected_kinds = {
        "user": inspect.Parameter.POSITIONAL_ONLY,
        "role": inspect.Parameter.POSITIONAL_OR_KEYWORD,
        "active": inspect.Parameter.KEYWORD_ONLY,
        "extra": inspect.Parameter.VAR_KEYWORD,
    }
    assert kinds == expected_kinds, f"expected={expected_kinds!r} actual={kinds!r}"

    with pytest.raises(TypeError):
        mod.format_user(user="ana")

    with pytest.raises(TypeError):
        mod.format_user("ana", "admin", False)


def test_defaults_are_correct():
    mod = _load_module()
    sig = inspect.signature(mod.format_user)
    defaults = {name: p.default for name, p in sig.parameters.items()}
    expected_defaults = {"user": inspect._empty, "role": "member", "active": True, "extra": inspect._empty}
    assert defaults == expected_defaults, f"expected={expected_defaults!r} actual={defaults!r}"


def test_rejects_missing_required_user():
    mod = _load_module()
    with pytest.raises(TypeError):
        mod.format_user()