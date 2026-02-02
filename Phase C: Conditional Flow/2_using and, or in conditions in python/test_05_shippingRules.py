import importlib.util
import os
import sys
import types
import pytest


def _load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _exec_with_env(path, env):
    code = open(path, "r", encoding="utf-8").read()
    glb = dict(env)
    glb["__name__"] = "__main__"
    exec(compile(code, path, "exec"), glb, glb)


def test_importable():
    path = os.path.join(os.path.dirname(__file__), "05_shippingRules.py")
    assert os.path.exists(path), f"expected={True} actual={os.path.exists(path)}"
    _load_module_from_path("shipping_rules_mod", path)


def test_prints_free_for_premium_member(capsys):
    path = os.path.join(os.path.dirname(__file__), "05_shippingRules.py")
    _exec_with_env(
        path,
        {"cart_total": 45, "is_domestic": True, "is_premium_member": True},
    )
    out = capsys.readouterr().out.strip()
    assert out == "FREE", f"expected={'FREE'} actual={out}"


def test_prints_standard_when_not_eligible(capsys):
    path = os.path.join(os.path.dirname(__file__), "05_shippingRules.py")
    _exec_with_env(
        path,
        {"cart_total": 45, "is_domestic": True, "is_premium_member": False},
    )
    out = capsys.readouterr().out.strip()
    assert out == "STANDARD", f"expected={'STANDARD'} actual={out}"


@pytest.mark.parametrize(
    "cart_total,is_domestic,is_premium_member,expected",
    [
        (50, True, False, "FREE"),
        (49.99, True, False, "STANDARD"),
        (50, False, False, "STANDARD"),
        (0, False, True, "FREE"),
        (0, True, True, "FREE"),
        (100, False, True, "FREE"),
    ],
)
def test_rule_matrix(cart_total, is_domestic, is_premium_member, expected, capsys):
    path = os.path.join(os.path.dirname(__file__), "05_shippingRules.py")
    _exec_with_env(
        path,
        {
            "cart_total": cart_total,
            "is_domestic": is_domestic,
            "is_premium_member": is_premium_member,
        },
    )
    out = capsys.readouterr().out.strip()
    assert out == expected, f"expected={expected} actual={out}"