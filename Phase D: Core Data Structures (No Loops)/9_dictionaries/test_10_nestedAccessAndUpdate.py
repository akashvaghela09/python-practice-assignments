import importlib.util
import os
import sys


def _load_module():
    filename = "10_nestedAccessAndUpdate.py"
    module_name = "mod_10_nestedAccessAndUpdate"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_expected_output(capsys):
    _load_module()
    out = capsys.readouterr().out.strip().splitlines()
    expected = ["94110", "{'name': 'Riley', 'address': {'city': 'SF', 'zip': '94110'}, 'visits': 3}"]
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_customer_structure_and_updates():
    m = _load_module()
    expected = {"name": "Riley", "address": {"city": "SF", "zip": "94110"}, "visits": 3}
    actual = getattr(m, "customer", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_customer_not_mutated_wrong_fields():
    m = _load_module()
    customer = m.customer
    expected_name = "Riley"
    expected_city = "SF"
    assert customer.get("name") == expected_name, f"expected={expected_name!r} actual={customer.get('name')!r}"
    assert customer.get("address", {}).get("city") == expected_city, f"expected={expected_city!r} actual={customer.get('address', {}).get('city')!r}"