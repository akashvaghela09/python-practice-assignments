import importlib
import io
import contextlib
import pytest


def _run_module():
    mod = importlib.import_module("07_unpackIgnoringWithUnderscore")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return mod, buf.getvalue()


def test_outputs_order_id_and_amount_only():
    _, out = _run_module()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected=2 actual={len(lines)}"
    assert lines[0] == "order-17", f"expected={'order-17'} actual={lines[0]}"
    assert lines[1] == "49.99", f"expected={'49.99'} actual={lines[1]}"


def test_variables_exist_and_match_record():
    mod, _ = _run_module()
    assert hasattr(mod, "record"), "expected=has record actual=missing record"
    assert hasattr(mod, "order_id"), "expected=has order_id actual=missing order_id"
    assert hasattr(mod, "amount"), "expected=has amount actual=missing amount"
    assert mod.order_id == mod.record[0], f"expected={mod.record[0]} actual={mod.order_id}"
    assert mod.amount == mod.record[3], f"expected={mod.record[3]} actual={mod.amount}"


def test_no_extra_non_private_module_vars_created():
    mod, _ = _run_module()
    public_names = [n for n in dir(mod) if not n.startswith("_")]
    extras = set(public_names) - {"record", "order_id", "amount"}
    assert extras == set(), f"expected={set()} actual={extras}"