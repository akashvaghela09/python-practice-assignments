import importlib.util
import pathlib
import pytest


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "05_findAndReplaceSlices.py"
    spec = importlib.util.spec_from_file_location("m05_findAndReplaceSlices", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixed_value_and_type(capsys):
    m = load_module()
    assert hasattr(m, "fixed"), "expected fixed vs actual missing"
    assert isinstance(m.fixed, str), "expected str vs actual type"
    assert m.fixed == "I like Python!", f"expected {'I like Python!'} vs actual {m.fixed!r}"

    out = capsys.readouterr().out
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    assert lines, "expected printed output vs actual empty"
    assert lines[-1] == "I like Python!", f"expected {'I like Python!'} vs actual {lines[-1]!r}"


def test_indices_and_slicing_logic():
    m = load_module()
    assert hasattr(m, "s"), "expected s vs actual missing"
    assert hasattr(m, "start"), "expected start vs actual missing"
    assert hasattr(m, "end"), "expected end vs actual missing"

    assert isinstance(m.start, int), "expected int vs actual type"
    assert isinstance(m.end, int), "expected int vs actual type"
    assert 0 <= m.start <= len(m.s), "expected valid index vs actual out of range"
    assert 0 <= m.end <= len(m.s), "expected valid index vs actual out of range"
    assert m.start < m.end, "expected start<end vs actual invalid order"

    assert m.s[m.start:m.end] == "Java", f"expected {'Java'} vs actual {m.s[m.start:m.end]!r}"
    assert m.s[:m.start] + "Python" + m.s[m.end:] == "I like Python!", f"expected {'I like Python!'} vs actual {m.s[:m.start] + 'Python' + m.s[m.end:]!r}"


def test_no_replace_used_in_source():
    path = pathlib.Path(__file__).resolve().parent / "05_findAndReplaceSlices.py"
    src = path.read_text(encoding="utf-8")
    assert ".replace(" not in src, "expected no replace usage vs actual found"