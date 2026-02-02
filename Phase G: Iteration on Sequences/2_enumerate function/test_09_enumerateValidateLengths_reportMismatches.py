import importlib
import io
import contextlib
import re
import pytest


MODULE_NAME = "09_enumerateValidateLengths_reportMismatches"


def run_module_capture_output():
    mod = importlib.import_module(MODULE_NAME)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return buf.getvalue()


def parse_mismatch_lines(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    pat = re.compile(r"^Index\s+(\d+)\s+expected\s+(\d+)\s+got\s+(\d+)$")
    parsed = []
    for ln in lines:
        m = pat.match(ln)
        assert m is not None, f"expected={pat.pattern} actual={ln}"
        parsed.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return parsed


def compute_expected_mismatches(mod):
    mismatches = []
    for i, w in enumerate(mod.words):
        exp = mod.expected_lengths[i]
        act = len(w)
        if act != exp:
            mismatches.append((i, exp, act))
    return mismatches


def test_output_lines_match_expected_mismatches():
    out = run_module_capture_output()
    mod = importlib.import_module(MODULE_NAME)
    expected = compute_expected_mismatches(mod)
    actual = parse_mismatch_lines(out)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_no_extra_or_missing_lines_and_indices_valid():
    out = run_module_capture_output()
    mod = importlib.import_module(MODULE_NAME)
    expected = compute_expected_mismatches(mod)
    actual = parse_mismatch_lines(out)

    assert len(actual) == len(expected), f"expected={len(expected)} actual={len(actual)}"

    for idx, exp, act in actual:
        assert 0 <= idx < len(mod.words), f"expected={[0, len(mod.words)-1]} actual={idx}"
        assert exp == mod.expected_lengths[idx], f"expected={mod.expected_lengths[idx]} actual={exp}"
        assert act == len(mod.words[idx]), f"expected={len(mod.words[idx])} actual={act}"


def test_prints_only_mismatches_even_when_all_match(monkeypatch):
    mod = importlib.import_module(MODULE_NAME)

    monkeypatch.setattr(mod, "expected_lengths", [len(w) for w in mod.words], raising=False)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    out = buf.getvalue().strip()

    assert out == "", f"expected={''} actual={out}"


def test_prints_all_when_all_mismatch(monkeypatch):
    mod = importlib.import_module(MODULE_NAME)

    monkeypatch.setattr(mod, "expected_lengths", [len(w) + 1 for w in mod.words], raising=False)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    out = buf.getvalue()
    actual = parse_mismatch_lines(out)

    expected = []
    for i, w in enumerate(mod.words):
        exp = len(w) + 1
        act = len(w)
        expected.append((i, exp, act))

    assert actual == expected, f"expected={expected} actual={actual}"


def test_format_has_single_spaces_and_no_trailing_text():
    out = run_module_capture_output()
    lines = [ln for ln in out.splitlines() if ln.strip()]
    for ln in lines:
        assert ln == ln.strip(), f"expected={ln.strip()} actual={ln}"
        assert "  " not in ln, f"expected={False} actual={True}"
        assert ln.startswith("Index "), f"expected={'Index '} actual={ln[:6]}"