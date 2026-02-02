import importlib
import os
import sys
import pytest


def _run_module_capture_stdout(monkeypatch, tmp_path, module_name):
    monkeypatch.chdir(tmp_path)
    sys.modules.pop(module_name, None)
    if hasattr(sys, "path"):
        if "" not in sys.path:
            sys.path.insert(0, "")
    mod = importlib.import_module(module_name)
    return mod


def test_outputs_exact_grid_coordinates(capsys):
    import 08_nestedLoopsCoordinates  # noqa: F401,E999


def test_outputs_exact_grid_coordinates_content(capsys):
    import importlib
    import sys

    sys.modules.pop("08_nestedLoopsCoordinates", None)
    importlib.import_module("08_nestedLoopsCoordinates")
    out = capsys.readouterr().out

    expected_lines = ["(0,0)", "(0,1)", "(0,2)", "(1,0)", "(1,1)", "(1,2)"]
    expected = "\n".join(expected_lines) + "\n"

    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_nonempty_lines(capsys):
    import importlib
    import sys

    sys.modules.pop("08_nestedLoopsCoordinates", None)
    importlib.import_module("08_nestedLoopsCoordinates")
    out = capsys.readouterr().out

    lines = out.splitlines()
    nonempty = [ln for ln in lines if ln.strip() != ""]
    assert len(nonempty) == 6, f"expected={6!r} actual={len(nonempty)!r}"


def test_each_line_format_is_parenthesized_pair(capsys):
    import importlib
    import sys
    import re

    sys.modules.pop("08_nestedLoopsCoordinates", None)
    importlib.import_module("08_nestedLoopsCoordinates")
    out = capsys.readouterr().out

    lines = out.splitlines()
    nonempty = [ln for ln in lines if ln.strip() != ""]
    pat = re.compile(r"^\(\d+,\d+\)$")
    all_match = all(bool(pat.match(ln)) for ln in nonempty)
    assert all_match is True, f"expected={True!r} actual={all_match!r}"