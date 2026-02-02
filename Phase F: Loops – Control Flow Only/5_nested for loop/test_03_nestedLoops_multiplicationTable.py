import importlib.util
import os
import re
import sys


def load_module(path):
    module_name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_table_output(text):
    lines = [ln.rstrip("\n") for ln in text.splitlines() if ln.strip() != ""]
    return lines


def expected_lines(n, cell_width):
    lines = []
    for r in range(1, n + 1):
        row = []
        for c in range(1, n + 1):
            row.append(str(r * c).rjust(cell_width))
        lines.append(" ".join(row))
    return lines


def test_prints_correct_table(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_nestedLoops_multiplicationTable.py")
    mod = load_module(path)
    out = capsys.readouterr().out
    got = parse_table_output(out)

    n = getattr(mod, "n", None)
    cell_width = getattr(mod, "cell_width", None)

    assert isinstance(n, int)
    assert isinstance(cell_width, int)
    exp = expected_lines(n, cell_width)

    assert got == exp, f"expected={exp!r} actual={got!r}"


def test_table_lines_variable_matches_expected_structure(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_nestedLoops_multiplicationTable.py")
    mod = load_module(path)
    capsys.readouterr()

    assert hasattr(mod, "table_lines")
    got = mod.table_lines
    assert isinstance(got, list)
    assert all(isinstance(x, str) for x in got)

    n = mod.n
    cell_width = mod.cell_width
    exp = expected_lines(n, cell_width)

    assert got == exp, f"expected={exp!r} actual={got!r}"


def test_alignment_and_separators(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_nestedLoops_multiplicationTable.py")
    mod = load_module(path)
    out = capsys.readouterr().out
    lines = parse_table_output(out)

    n = mod.n
    cell_width = mod.cell_width
    exp = expected_lines(n, cell_width)

    assert len(lines) == n, f"expected={n!r} actual={len(lines)!r}"
    for i, (g, e) in enumerate(zip(lines, exp), start=1):
        assert g == e, f"expected={e!r} actual={g!r}"

        parts = g.split(" ")
        assert len(parts) == n, f"expected={n!r} actual={len(parts)!r}"
        assert all(len(p) == cell_width for p in parts), f"expected={cell_width!r} actual={[len(p) for p in parts]!r}"
        assert all(re.fullmatch(r"\s*\d+", p) for p in parts), f"expected={'digits'!r} actual={parts!r}"


def test_no_trailing_extra_spaces_per_line(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_nestedLoops_multiplicationTable.py")
    _ = load_module(path)
    out = capsys.readouterr().out
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]

    trailing = [ln for ln in lines if ln.endswith(" ")]
    assert trailing == [], f"expected={[]!r} actual={trailing!r}"