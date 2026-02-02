import importlib.util
import io
import os
import sys
from pathlib import Path

import pytest


MODULE_FILENAME = "10_moneyWithDecimals.py"


def _load_module_from_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_expected_output_lines(capsys):
    file_path = Path(__file__).resolve().parent / MODULE_FILENAME
    assert file_path.exists()

    mod_name = f"student_mod_{file_path.stem}"

    _load_module_from_path(file_path, mod_name)

    out = capsys.readouterr().out
    lines = [ln.rstrip("\n") for ln in out.splitlines() if ln.strip() != ""]
    expected = ["0.3", "0.30", "3.50"]

    assert len(lines) == len(expected), f"expected={len(expected)} actual={len(lines)}"
    for i, (act, exp) in enumerate(zip(lines, expected)):
        assert act == exp, f"expected={exp} actual={act}"


def test_file_has_no_placeholders():
    file_path = Path(__file__).resolve().parent / MODULE_FILENAME
    src = file_path.read_text(encoding="utf-8")
    assert "__________" not in src, "expected=no_placeholders actual=placeholders_found"


def test_module_importable_by_filename(capsys):
    file_path = Path(__file__).resolve().parent / MODULE_FILENAME
    mod_name = "mod_import_check"

    _load_module_from_path(file_path, mod_name)
    out = capsys.readouterr().out
    assert out is not None, "expected=some_output actual=None"