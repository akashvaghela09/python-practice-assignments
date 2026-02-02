import io
import runpy
import builtins
import pytest


MODULE = "06_firstMultipleOf7"


def run_program(inputs):
    it = iter(inputs)

    def fake_input(prompt=None):
        return next(it)

    buf = io.StringIO()
    old_input = builtins.input
    old_stdout = __import__("sys").stdout
    try:
        builtins.input = fake_input
        __import__("sys").stdout = buf
        runpy.run_module(MODULE, run_name="__main__")
    finally:
        builtins.input = old_input
        __import__("sys").stdout = old_stdout
    return buf.getvalue()


def first_multiple_of_7(start, end):
    for x in range(start, end + 1):
        if x % 7 == 0:
            return x
    return None


@pytest.mark.parametrize(
    "start,end",
    [
        (10, 30),
        (1, 6),
        (7, 7),
        (8, 13),
        (8, 14),
        (0, 0),
        (-20, -1),
        (-14, -1),
        (-13, -8),
        (-1, 1),
        (1, 100),
        (14, 20),
        (15, 20),
    ],
)
def test_first_multiple_of_7_various_ranges(start, end):
    out = run_program([str(start), str(end)]).strip()
    expected = first_multiple_of_7(start, end)
    expected_str = "None" if expected is None else str(expected)
    assert out == expected_str, f"expected={expected_str} actual={out}"


def test_output_single_line_no_extra_tokens():
    start, end = 10, 30
    out = run_program([str(start), str(end)])
    stripped = out.strip()
    expected = first_multiple_of_7(start, end)
    expected_str = "None" if expected is None else str(expected)
    assert stripped == expected_str, f"expected={expected_str} actual={stripped}"
    tokens = stripped.split()
    assert len(tokens) == 1, f"expected=1_token actual={len(tokens)}"


def test_reads_exactly_two_inputs():
    start, end = 1, 6
    inputs = [str(start), str(end), "9999"]
    out = run_program(inputs).strip()
    expected = first_multiple_of_7(start, end)
    expected_str = "None" if expected is None else str(expected)
    assert out == expected_str, f"expected={expected_str} actual={out}"