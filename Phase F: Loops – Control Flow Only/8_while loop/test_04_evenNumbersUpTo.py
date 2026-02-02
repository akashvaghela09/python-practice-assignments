import importlib
import io
import contextlib
import re
import pytest


MODULE_NAME = "04_evenNumbersUpTo"


def _run_module_capture_stdout():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.invalidate_caches()
        importlib.import_module(MODULE_NAME)
    return buf.getvalue()


def test_prints_even_numbers_up_to_12_exact_lines():
    out = _run_module_capture_stdout()
    expected = "2\n4\n6\n8\n10\n12\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_whitespace_or_blank_lines():
    out = _run_module_capture_stdout()
    expected_lines = ["2", "4", "6", "8", "10", "12"]
    actual_lines = out.splitlines()
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_only_integers_printed_and_all_even():
    out = _run_module_capture_stdout()
    tokens = out.split()
    expected_count = 6
    assert len(tokens) == expected_count, f"expected={expected_count!r} actual={len(tokens)!r}"

    ints = []
    for t in tokens:
        assert re.fullmatch(r"-?\d+", t) is not None, f"expected={'integer token'!r} actual={t!r}"
        ints.append(int(t))

    expected_all_even = True
    actual_all_even = all(x % 2 == 0 for x in ints)
    assert actual_all_even == expected_all_even, f"expected={expected_all_even!r} actual={actual_all_even!r}"


def test_sequence_is_strictly_increasing_by_2_and_starts_at_2():
    out = _run_module_capture_stdout()
    seq = [int(x) for x in out.split()]
    expected_start = 2
    actual_start = seq[0] if seq else None
    assert actual_start == expected_start, f"expected={expected_start!r} actual={actual_start!r}"

    expected_diffs = [2] * (len(seq) - 1)
    actual_diffs = [b - a for a, b in zip(seq, seq[1:])]
    assert actual_diffs == expected_diffs, f"expected={expected_diffs!r} actual={actual_diffs!r}"

    expected_end = 12
    actual_end = seq[-1] if seq else None
    assert actual_end == expected_end, f"expected={expected_end!r} actual={actual_end!r}"


def test_module_imports_without_error():
    try:
        _run_module_capture_stdout()
        ok = True
    except Exception:
        ok = False
    assert ok is True, f"expected={True!r} actual={ok!r}"