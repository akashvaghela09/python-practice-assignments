import importlib
import io
import os
import sys


def test_output_role_and_default_logins(capsys):
    module_name = "03_safeGetDefault"
    if module_name in sys.modules:
        del sys.modules[module_name]

    importlib.import_module(module_name)
    out = capsys.readouterr().out

    lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    expected_lines = ["guest", "0"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"


def test_uses_get_with_default_for_logins():
    file_path = os.path.join(os.path.dirname(__file__), "03_safeGetDefault.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    expected_snippets = ['get("logins", 0)', "get('logins', 0)"]
    found = any(snip in src for snip in expected_snippets)
    assert found, f"expected={True!r} actual={found!r}"


def test_no_direct_key_access_for_logins():
    file_path = os.path.join(os.path.dirname(__file__), "03_safeGetDefault.py")
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    bad_patterns = ['["logins"]', "['logins']"]
    present = any(pat in src for pat in bad_patterns)
    assert present is False, f"expected={False!r} actual={present!r}"