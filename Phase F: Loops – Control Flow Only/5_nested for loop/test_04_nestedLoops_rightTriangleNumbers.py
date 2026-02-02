import importlib
import sys
import pytest

MODULE_NAME = "04_nestedLoops_rightTriangleNumbers"

def run_module_capture(capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    importlib.import_module(MODULE_NAME)
    out = capsys.readouterr().out
    return out

def expected_triangle(rows):
    return "\n".join("".join(str(n) for n in range(1, i + 1)) for i in range(1, rows + 1))

def test_prints_correct_triangle_output(capsys):
    out = run_module_capture(capsys)
    exp = expected_triangle(5) + "\n"
    assert out == exp, f"expected={exp!r} actual={out!r}"

def test_output_has_correct_number_of_lines(capsys):
    out = run_module_capture(capsys)
    lines = out.splitlines()
    assert len(lines) == 5, f"expected={5!r} actual={len(lines)!r}"

@pytest.mark.parametrize("i", [1, 2, 3, 4, 5])
def test_each_line_is_increasing_sequence(capsys, i):
    out = run_module_capture(capsys)
    lines = out.splitlines()
    assert lines[i - 1] == "".join(str(n) for n in range(1, i + 1)), (
        f"expected={''.join(str(n) for n in range(1, i + 1))!r} actual={lines[i - 1]!r}"
    )

def test_no_extra_whitespace_or_spaces_in_lines(capsys):
    out = run_module_capture(capsys)
    lines = out.splitlines()
    bad = [ln for ln in lines if ln.strip() != ln or " " in ln or "\t" in ln or "\r" in ln]
    assert bad == [], f"expected={[]!r} actual={bad!r}"

def test_no_trailing_blank_lines_beyond_final_newline(capsys):
    out = run_module_capture(capsys)
    exp = expected_triangle(5) + "\n"
    assert out == exp, f"expected={exp!r} actual={out!r}"