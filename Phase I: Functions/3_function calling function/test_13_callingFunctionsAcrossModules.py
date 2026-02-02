import importlib
import os
import sys
from pathlib import Path


def _ensure_utils_math(module_dir: Path):
    module_dir.mkdir(parents=True, exist_ok=True)
    utils_path = module_dir / "utils_math.py"
    if not utils_path.exists():
        utils_path.write_text(
            "def multiply(a, b):\n"
            "    return a * b\n",
            encoding="utf-8",
        )
    return utils_path


def _import_target(tmp_path, monkeypatch):
    src = Path(__file__).resolve().parent
    target_src = src / "13_callingFunctionsAcrossModules.py"
    assert target_src.exists()

    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    target_dst = work_dir / "13_callingFunctionsAcrossModules.py"
    target_dst.write_text(target_src.read_text(encoding="utf-8"), encoding="utf-8")

    _ensure_utils_math(work_dir)

    monkeypatch.chdir(work_dir)
    monkeypatch.syspath_prepend(str(work_dir))

    mod = importlib.import_module("13_callingFunctionsAcrossModules")
    return mod


def test_prints_expected_value(capsys, tmp_path, monkeypatch):
    _import_target(tmp_path, monkeypatch)
    out = capsys.readouterr().out.strip()
    assert out == "35", f"expected='35' actual={out!r}"


def test_area_rectangle_uses_utils_math_multiply(tmp_path, monkeypatch):
    mod = _import_target(tmp_path, monkeypatch)

    called = {"n": 0, "args": None}

    def spy(a, b):
        called["n"] += 1
        called["args"] = (a, b)
        return a * b

    mod.multiply = spy
    res = mod.area_rectangle(5, 7)

    assert called["n"] == 1, f"expected=1 actual={called['n']!r}"
    assert called["args"] == (5, 7), f"expected={(5, 7)!r} actual={called['args']!r}"
    assert res == 35, f"expected=35 actual={res!r}"


def test_area_rectangle_returns_correct_for_various_inputs(tmp_path, monkeypatch):
    mod = _import_target(tmp_path, monkeypatch)

    cases = [
        (0, 10, 0),
        (3, 4, 12),
        (-3, 4, -12),
        (2.5, 4, 10.0),
    ]
    for w, h, expected in cases:
        actual = mod.area_rectangle(w, h)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"