import importlib
import re
import sys

import pytest


def _load_module():
    name = "03_sumNumbers"
    if name in sys.modules:
        return importlib.reload(sys.modules[name])
    return importlib.import_module(name)


def _extract_last_int(output: str):
    ints = re.findall(r"-?\d+", output)
    return int(ints[-1]) if ints else None


def test_prints_total_15(capsys):
    _load_module()
    out = capsys.readouterr().out.strip()
    actual = _extract_last_int(out)
    expected = 15
    assert actual == expected, f"expected={expected} actual={actual}"


def test_outputs_single_line(capsys):
    _load_module()
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    actual = len(lines)
    expected = 1
    assert actual == expected, f"expected={expected} actual={actual}"


def test_last_line_is_number_only(capsys):
    _load_module()
    out = capsys.readouterr().out
    last = [ln for ln in out.splitlines() if ln.strip() != ""][-1].strip()
    actual = bool(re.fullmatch(r"-?\d+", last))
    expected = True
    assert actual == expected, f"expected={expected} actual={actual}"


def test_total_matches_sum_of_nums(capsys):
    mod = _load_module()
    out = capsys.readouterr().out.strip()
    actual = _extract_last_int(out)
    expected = sum(getattr(mod, "nums", []))
    assert actual == expected, f"expected={expected} actual={actual}"