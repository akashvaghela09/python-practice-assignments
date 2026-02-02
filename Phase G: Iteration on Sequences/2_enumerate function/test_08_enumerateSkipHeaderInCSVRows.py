import importlib
import io
import sys
import contextlib
import pytest


def _run_module_capture_stdout(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(module_name)
    return buf.getvalue()


def test_output_matches_expected_lines():
    out = _run_module_capture_stdout("08_enumerateSkipHeaderInCSVRows")
    got = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    expected = ["1: Alice", "2: Bob"]
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_does_not_print_header():
    out = _run_module_capture_stdout("08_enumerateSkipHeaderInCSVRows")
    got = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    unexpected = "name"
    assert all(unexpected not in line for line in got), f"expected={False!r} actual={any(unexpected in line for line in got)!r}"


def test_enumeration_starts_at_one_and_is_sequential():
    out = _run_module_capture_stdout("08_enumerateSkipHeaderInCSVRows")
    got = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    nums = []
    for line in got:
        if ":" not in line:
            pytest.fail(f"expected={True!r} actual={False!r}")
        left = line.split(":", 1)[0].strip()
        assert left.isdigit(), f"expected={True!r} actual={left.isdigit()!r}"
        nums.append(int(left))
    expected_nums = list(range(1, len(got) + 1))
    assert nums == expected_nums, f"expected={expected_nums!r} actual={nums!r}"


def test_prints_only_name_not_age():
    out = _run_module_capture_stdout("08_enumerateSkipHeaderInCSVRows")
    got = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    for line in got:
        right = line.split(":", 1)[1].strip() if ":" in line else ""
        assert "," not in right, f"expected={False!r} actual={( ',' in right )!r}"
        assert right and not any(ch.isdigit() for ch in right), f"expected={False!r} actual={any(ch.isdigit() for ch in right)!r}"