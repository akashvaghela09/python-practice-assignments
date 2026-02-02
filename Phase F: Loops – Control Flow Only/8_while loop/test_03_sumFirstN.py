import importlib.util
import os
import re
import sys
import pytest

FILE_NAME = "03_sumFirstN.py"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("sum_first_n_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    old_stdout = sys.stdout
    try:
        from io import StringIO

        buf = StringIO()
        sys.stdout = buf
        spec = importlib.util.spec_from_file_location("sum_first_n_run", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return buf.getvalue(), mod
    finally:
        sys.stdout = old_stdout


def test_script_runs_without_placeholder_syntaxerror():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "__________" not in src, f"expected no placeholders vs actual placeholders_present={('__________' in src)}"
    compile(src, path, "exec")


def test_output_matches_expected_sum_line():
    out, _ = _run_script_capture_stdout()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]

    assert len(lines) == 1, f"expected lines=1 vs actual lines={len(lines)}"
    line = lines[0]

    m = re.fullmatch(r"Sum is\s+(-?\d+)", line)
    assert m is not None, f"expected format='Sum is <int>' vs actual line={line!r}"

    actual_total = int(m.group(1))
    expected_total = sum(range(1, 10 + 1))
    assert actual_total == expected_total, f"expected total={expected_total} vs actual total={actual_total}"


def test_uses_while_loop_not_for_loop():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    assert "while" in src, f"expected while_present=True vs actual while_present={('while' in src)}"
    assert "for " not in src, f"expected for_present=False vs actual for_present={('for ' in src)}"
    assert "range(" not in src, f"expected range_present=False vs actual range_present={('range(' in src)}"


def test_variables_updated_and_total_consistent():
    _, mod = _run_script_capture_stdout()

    assert hasattr(mod, "limit"), f"expected has_limit=True vs actual has_limit={hasattr(mod, 'limit')}"
    assert hasattr(mod, "total"), f"expected has_total=True vs actual has_total={hasattr(mod, 'total')}"
    assert hasattr(mod, "current"), f"expected has_current=True vs actual has_current={hasattr(mod, 'current')}"

    expected_total = sum(range(1, int(mod.limit) + 1))
    actual_total = int(mod.total)

    assert actual_total == expected_total, f"expected total={expected_total} vs actual total={actual_total}"
    assert int(mod.current) == int(mod.limit) + 1, f"expected current={int(mod.limit)+1} vs actual current={int(mod.current)}"