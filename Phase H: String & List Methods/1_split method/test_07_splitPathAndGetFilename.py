import importlib.util
import os
import sys
from pathlib import Path


def _load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_filename_only(capsys):
    file_path = Path(__file__).resolve().parent / "07_splitPathAndGetFilename.py"
    assert file_path.exists()

    _load_module_from_path("mod07_splitPathAndGetFilename", file_path)
    out = capsys.readouterr().out
    got_lines = [line for line in out.splitlines() if line.strip() != ""]
    assert len(got_lines) == 1
    got = got_lines[0]
    expected = os.path.basename("/home/alex/docs/notes.txt")
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_does_not_print_path_separators(capsys):
    file_path = Path(__file__).resolve().parent / "07_splitPathAndGetFilename.py"
    _load_module_from_path("mod07_splitPathAndGetFilename_2", file_path)
    out = capsys.readouterr().out
    got_lines = [line for line in out.splitlines() if line.strip() != ""]
    got = got_lines[-1] if got_lines else ""
    expected = False
    actual = ("/" in got) or ("\\" in got)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_has_no_extra_whitespace(capsys):
    file_path = Path(__file__).resolve().parent / "07_splitPathAndGetFilename.py"
    _load_module_from_path("mod07_splitPathAndGetFilename_3", file_path)
    out = capsys.readouterr().out
    got_lines = [line for line in out.splitlines() if line.strip() != ""]
    got = got_lines[0] if got_lines else ""
    expected = got.strip()
    actual = got
    assert actual == expected, f"expected={expected!r} actual={actual!r}"