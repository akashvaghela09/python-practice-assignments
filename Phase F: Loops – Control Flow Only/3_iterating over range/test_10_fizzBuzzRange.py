import io
import os
import sys
import runpy
import pytest

MODULE_NAME = "10_fizzBuzzRange"


def run_module_with_input(monkeypatch, inputs):
    data = "\n".join(str(x) for x in inputs) + "\n"
    monkeypatch.setattr(sys, "stdin", io.StringIO(data))
    out = io.StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    runpy.run_module(MODULE_NAME, run_name="__main__")
    return out.getvalue()


def expected_lines(start, end):
    res = []
    for n in range(start, end + 1):
        if n % 3 == 0 and n % 5 == 0:
            res.append("FizzBuzz")
        elif n % 3 == 0:
            res.append("Fizz")
        elif n % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(n))
    return res


def assert_output(monkeypatch, start, end):
    actual = run_module_with_input(monkeypatch, [start, end]).splitlines()
    exp = expected_lines(start, end)
    assert actual == exp, f"expected={exp!r} actual={actual!r}"


@pytest.mark.parametrize(
    "start,end",
    [
        (14, 16),
        (1, 1),
        (1, 15),
        (3, 5),
        (15, 15),
        (-5, 5),
        (-16, -14),
        (0, 0),
        (0, 16),
        (30, 33),
    ],
)
def test_fizzbuzz_range_various(monkeypatch, start, end):
    assert_output(monkeypatch, start, end)


def test_inclusive_range_end(monkeypatch):
    start, end = 8, 10
    out = run_module_with_input(monkeypatch, [start, end]).splitlines()
    exp = expected_lines(start, end)
    assert out == exp, f"expected={exp!r} actual={out!r}"
    assert len(out) == (end - start + 1), f"expected={end - start + 1!r} actual={len(out)!r}"


def test_single_value_non_multiple(monkeypatch):
    start, end = 7, 7
    out = run_module_with_input(monkeypatch, [start, end]).splitlines()
    exp = expected_lines(start, end)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_single_value_fizzbuzz(monkeypatch):
    start, end = 45, 45
    out = run_module_with_input(monkeypatch, [start, end]).splitlines()
    exp = expected_lines(start, end)
    assert out == exp, f"expected={exp!r} actual={out!r}"


def test_no_extra_whitespace_lines(monkeypatch):
    start, end = 1, 20
    raw = run_module_with_input(monkeypatch, [start, end])
    assert raw.endswith("\n"), f"expected={True!r} actual={raw.endswith(chr(10))!r}"
    lines = raw.splitlines()
    exp = expected_lines(start, end)
    assert lines == exp, f"expected={exp!r} actual={lines!r}"
    assert all(line != "" for line in lines), f"expected={True!r} actual={any(line == '' for line in lines)!r}"


def test_source_has_no_blanks_left():
    here = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
    path = os.path.join(here, f"{MODULE_NAME}.py")
    if not os.path.exists(path):
        path = f"{MODULE_NAME}.py"
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    assert "____" not in src, f"expected={False!r} actual={('____' in src)!r}"