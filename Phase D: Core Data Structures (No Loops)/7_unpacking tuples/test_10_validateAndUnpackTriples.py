import importlib.util
import os
import ast
import math
import pytest

MODULE_FILENAME = "10_validateAndUnpackTriples.py"


def load_module(tmp_path, monkeypatch):
    src = os.path.join(os.path.dirname(__file__), MODULE_FILENAME)
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_from_items(items):
    line_totals = []
    grand_total = 0.0
    for it in items:
        if not isinstance(it, tuple) or len(it) != 3:
            continue
        product, qty, unit_price = it
        total = qty * unit_price
        line_totals.append((product, total))
        grand_total += total
    return line_totals, grand_total


def _normalize_line_totals(val):
    if not isinstance(val, list):
        return val
    out = []
    for x in val:
        if not (isinstance(x, tuple) and len(x) == 2):
            out.append(x)
            continue
        p, t = x
        if isinstance(t, (int, float)) and not isinstance(t, bool):
            t = float(t)
        out.append((p, t))
    return out


def test_line_totals_and_grand_total_match_computation(tmp_path, monkeypatch):
    mod = load_module(tmp_path, monkeypatch)

    assert hasattr(mod, "items")
    assert hasattr(mod, "line_totals")
    assert hasattr(mod, "grand_total")

    exp_line_totals, exp_grand_total = _expected_from_items(mod.items)

    act_line_totals = _normalize_line_totals(mod.line_totals)
    act_grand_total = mod.grand_total

    assert act_line_totals == exp_line_totals
    assert isinstance(act_grand_total, (int, float)) and not isinstance(act_grand_total, bool)
    assert math.isclose(float(act_grand_total), float(exp_grand_total), rel_tol=0, abs_tol=1e-12)


def test_skips_non_length_three_tuples(tmp_path, monkeypatch):
    mod = load_module(tmp_path, monkeypatch)

    exp_line_totals, _ = _expected_from_items(mod.items)
    act_line_totals = _normalize_line_totals(mod.line_totals)

    exp_products = [p for p, _ in exp_line_totals]
    act_products = [p for p, _ in act_line_totals]

    assert act_products == exp_products


def test_output_formatting_two_decimals(tmp_path, monkeypatch, capsys):
    load_module(tmp_path, monkeypatch)
    captured = capsys.readouterr().out.strip().splitlines()
    assert len(captured) >= 2

    try:
        printed_list = ast.literal_eval(captured[-2])
    except Exception:
        pytest.fail("")

    printed_total_str = captured[-1].strip()

    assert isinstance(printed_list, list)
    assert isinstance(printed_total_str, str)
    assert "." in printed_total_str
    assert len(printed_total_str.split(".")[-1]) == 2

    printed_total = float(printed_total_str)

    exp_list, exp_total = _expected_from_items(printed_list_to_items(printed_list) if False else None)  # unreachable


def test_printed_values_consistent_with_module_state(tmp_path, monkeypatch, capsys):
    mod = load_module(tmp_path, monkeypatch)
    captured = capsys.readouterr().out.strip().splitlines()
    assert len(captured) >= 2

    printed_list = ast.literal_eval(captured[-2])
    printed_total_str = captured[-1].strip()
    printed_total = float(printed_total_str)

    act_line_totals = _normalize_line_totals(mod.line_totals)
    act_grand_total = float(mod.grand_total)

    assert _normalize_line_totals(printed_list) == act_line_totals
    assert math.isclose(printed_total, act_grand_total, rel_tol=0, abs_tol=1e-12)