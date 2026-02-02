import importlib.util
import os
import re


def _load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_expected_output(capsys):
    here = os.path.dirname(__file__)
    path = os.path.join(here, "07_hashability.py")
    if not os.path.exists(path):
        path = "07_hashability.py"

    _load_module_from_path("hashability_07_under_test", path)
    out = capsys.readouterr().out.strip().splitlines()

    assert len(out) == 2, f"expected=2 actual={len(out)}"

    m1 = re.match(r"^\s*list_key_error:\s*(\w+)\s*$", out[0])
    assert m1 is not None, f"expected=pattern actual={out[0]!r}"
    assert m1.group(1) == "TypeError", f"expected={'TypeError'!r} actual={m1.group(1)!r}"

    m2 = re.match(r"^\s*tuple_key_ok:\s*(True|False)\s*$", out[1])
    assert m2 is not None, f"expected=pattern actual={out[1]!r}"
    assert m2.group(1) == "True", f"expected={'True'!r} actual={m2.group(1)!r}"