import importlib
import io
import sys


def run_module_capture(name):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        importlib.invalidate_caches()
        if name in sys.modules:
            del sys.modules[name]
        importlib.import_module(name)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_prints_first_x_position_in_row_and_continues_outer_loop():
    out = run_module_capture("08_search2DGridBreakInner")
    expected = "1,2\n2,0\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output():
    out = run_module_capture("08_search2DGridBreakInner")
    expected_lines = ["1,2", "2,0"]
    actual_lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_output_format_row_col_integers():
    out = run_module_capture("08_search2DGridBreakInner")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip() != ""]
    expected_count = 2
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"
    parsed = []
    for ln in lines:
        parts = ln.split(",")
        parsed.append(parts)
        assert len(parts) == 2, f"expected={2!r} actual={len(parts)!r}"
        assert parts[0].isdigit() and parts[1].isdigit(), f"expected={True!r} actual={(parts[0].isdigit() and parts[1].isdigit())!r}"
    expected_parsed = [["1", "2"], ["2", "0"]]
    assert parsed == expected_parsed, f"expected={expected_parsed!r} actual={parsed!r}"