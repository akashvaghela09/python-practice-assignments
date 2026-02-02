import importlib
import io
import contextlib
import re


def _run_module():
    mod_name = "06_frozensetBasics"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    return buf.getvalue()


def test_output_contains_2_true():
    out = _run_module()
    assert re.search(r"contains 2\?\s*True\s*$", out, re.MULTILINE), f"expected contains-true, got: {out!r}"


def test_output_union_size_4():
    out = _run_module()
    assert re.search(r"union size:\s*4\s*$", out, re.MULTILINE), f"expected union-size-4, got: {out!r}"


def test_exact_two_lines():
    out = _run_module()
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 2, f"expected 2 lines, got: {lines!r}"
    assert lines[0].startswith("contains 2?"), f"expected contains line, got: {lines[0]!r}"
    assert lines[1].startswith("union size:"), f"expected union line, got: {lines[1]!r}"