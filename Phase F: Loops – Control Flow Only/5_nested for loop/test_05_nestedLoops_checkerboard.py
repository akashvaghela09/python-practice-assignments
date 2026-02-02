import importlib.util
import os
import sys


def _load_module():
    fname = "05_nestedLoops_checkerboard.py"
    path = os.path.join(os.path.dirname(__file__), fname)
    spec = importlib.util.spec_from_file_location("checkerboard_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected_checkerboard(size):
    return "\n".join(
        "".join("X" if (r + c) % 2 == 0 else "." for c in range(size))
        for r in range(size)
    )


def test_printed_output_matches_expected(capfd):
    mod = _load_module()
    out = capfd.readouterr().out.rstrip("\n")
    expected = _expected_checkerboard(getattr(mod, "size", 5))
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_lines_variable_exists_and_is_correct_type_and_length(capfd):
    mod = _load_module()
    capfd.readouterr()
    assert hasattr(mod, "lines"), "expected=True actual=False"
    assert isinstance(mod.lines, list), f"expected={list.__name__!r} actual={type(mod.lines).__name__!r}"
    expected_len = getattr(mod, "size", 5)
    assert len(mod.lines) == expected_len, f"expected={expected_len!r} actual={len(mod.lines)!r}"


def test_lines_rows_have_correct_width_and_characters(capfd):
    mod = _load_module()
    capfd.readouterr()
    size = getattr(mod, "size", 5)
    assert all(isinstance(row, str) for row in mod.lines), f"expected={'all_str'!r} actual={'not_all_str'!r}"
    widths = [len(row) for row in mod.lines]
    assert widths == [size] * size, f"expected={[size]*size!r} actual={widths!r}"
    allowed = {"X", "."}
    invalid = sorted({ch for row in mod.lines for ch in row if ch not in allowed})
    assert invalid == [], f"expected={[]!r} actual={invalid!r}"


def test_pattern_parity_correct_at_multiple_positions(capfd):
    mod = _load_module()
    capfd.readouterr()
    size = getattr(mod, "size", 5)
    expected_lines = _expected_checkerboard(size).splitlines()
    actual_lines = mod.lines
    mismatches = []
    for r in range(size):
        for c in range(size):
            if actual_lines[r][c] != expected_lines[r][c]:
                mismatches.append((r, c, expected_lines[r][c], actual_lines[r][c]))
                if len(mismatches) >= 5:
                    break
        if len(mismatches) >= 5:
            break
    assert mismatches == [], f"expected={[]} actual={mismatches!r}"


def test_printed_output_equals_join_of_lines(capfd):
    mod = _load_module()
    out = capfd.readouterr().out.rstrip("\n")
    joined = "\n".join(mod.lines)
    assert out == joined, f"expected={joined!r} actual={out!r}"