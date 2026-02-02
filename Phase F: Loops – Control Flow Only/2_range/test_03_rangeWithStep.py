import importlib.util
import os
import sys
import ast
import pytest


ASSIGNMENT_FILE = "03_rangeWithStep.py"


def _load_module(tmp_path, monkeypatch):
    src = os.path.join(os.path.dirname(__file__), ASSIGNMENT_FILE)
    dst = tmp_path / ASSIGNMENT_FILE
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [ASSIGNMENT_FILE])

    spec = importlib.util.spec_from_file_location("mod03_rangeWithStep", str(dst))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_evens_value(tmp_path, monkeypatch, capsys):
    mod = _load_module(tmp_path, monkeypatch)
    expected = [0, 2, 4, 6, 8, 10]
    actual = getattr(mod, "evens", None)
    assert actual == expected, f"expected={expected} actual={actual}"

    out = capsys.readouterr().out.strip()
    assert out, f"expected={str(expected)} actual={out}"
    try:
        printed = ast.literal_eval(out)
    except Exception:
        pytest.fail(f"expected={str(expected)} actual={out}")
    assert printed == expected, f"expected={expected} actual={printed}"


def test_evens_uses_range_with_step(tmp_path, monkeypatch):
    src = os.path.join(os.path.dirname(__file__), ASSIGNMENT_FILE)
    tree = ast.parse(open(src, "r", encoding="utf-8").read())

    call = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "evens":
                    call = node.value
                    break

    assert call is not None, f"expected={'evens assignment'} actual={None}"
    assert isinstance(call, ast.Call), f"expected={'Call'} actual={type(call).__name__}"
    assert isinstance(call.func, ast.Name) and call.func.id == "list", f"expected={'list(...)'} actual={ast.dump(call, include_attributes=False)}"
    assert len(call.args) == 1, f"expected={1} actual={len(call.args)}"

    inner = call.args[0]
    assert isinstance(inner, ast.Call), f"expected={'range(...)'} actual={type(inner).__name__}"
    assert isinstance(inner.func, ast.Name) and inner.func.id == "range", f"expected={'range'} actual={ast.dump(inner.func, include_attributes=False)}"
    assert len(inner.args) == 3, f"expected={3} actual={len(inner.args)}"