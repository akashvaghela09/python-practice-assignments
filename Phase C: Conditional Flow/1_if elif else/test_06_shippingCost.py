import importlib.util
import os
import re
import sys


def _run_module_capture_stdout(monkeypatch, weight, member):
    path = os.path.join(os.path.dirname(__file__), "06_shippingCost.py")
    spec = importlib.util.spec_from_file_location("shipping_cost_mod", path)
    mod = importlib.util.module_from_spec(spec)

    out = []

    def _fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        out.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", _fake_print)
    mod.weight = weight
    mod.member = member
    sys.modules["shipping_cost_mod"] = mod
    spec.loader.exec_module(mod)

    return "".join(out)


def _expected_output(weight, member):
    if weight <= 0:
        return "Invalid weight"
    if member:
        if weight <= 2:
            return "Shipping cost: 0"
        if weight <= 5:
            return "Shipping cost: 3"
        return "Shipping cost: 7"
    else:
        if weight <= 2:
            return "Shipping cost: 5"
        if weight <= 5:
            return "Shipping cost: 8"
        return "Shipping cost: 12"


def _normalize(output):
    return output.strip()


def _parse_cost(output):
    m = re.search(r"Shipping cost:\s*(-?\d+)\s*$", output.strip())
    if not m:
        return None
    return int(m.group(1))


def test_invalid_weight_negative(monkeypatch):
    actual = _normalize(_run_module_capture_stdout(monkeypatch, -1, False))
    expected = _expected_output(-1, False)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_invalid_weight_zero(monkeypatch):
    actual = _normalize(_run_module_capture_stdout(monkeypatch, 0, True))
    expected = _expected_output(0, True)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_member_boundary_2(monkeypatch):
    w = 2
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, True))
    expected = _expected_output(w, True)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_member_just_over_2(monkeypatch):
    w = 2.0001
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, True))
    expected = _expected_output(w, True)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_member_boundary_5(monkeypatch):
    w = 5
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, True))
    expected = _expected_output(w, True)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_member_over_5(monkeypatch):
    w = 5.01
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, True))
    expected = _expected_output(w, True)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_non_member_boundary_2(monkeypatch):
    w = 2
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, False))
    expected = _expected_output(w, False)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_non_member_just_over_2(monkeypatch):
    w = 2.0001
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, False))
    expected = _expected_output(w, False)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_non_member_boundary_5(monkeypatch):
    w = 5
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, False))
    expected = _expected_output(w, False)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_non_member_over_5(monkeypatch):
    w = 10
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, False))
    expected = _expected_output(w, False)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_expected_example_case(monkeypatch):
    w = 4.5
    m = False
    actual = _normalize(_run_module_capture_stdout(monkeypatch, w, m))
    expected = _expected_output(w, m)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_format_either_invalid_or_shipping_cost(monkeypatch):
    cases = [
        (-1, False),
        (1, True),
        (3, False),
        (6, True),
    ]
    for w, m in cases:
        out = _normalize(_run_module_capture_stdout(monkeypatch, w, m))
        is_invalid = out == "Invalid weight"
        is_cost = _parse_cost(out) is not None
        assert (is_invalid or is_cost), f"expected={('Invalid weight OR Shipping cost: <number>')} actual={out!r}"