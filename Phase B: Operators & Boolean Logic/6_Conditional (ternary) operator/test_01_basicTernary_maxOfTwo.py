import importlib.util
import os
import sys
from pathlib import Path


def _load_module_from_path(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_output_exact(capsys):
    target = Path(__file__).resolve().parent / "01_basicTernary_maxOfTwo.py"
    if not target.exists():
        target = Path.cwd() / "01_basicTernary_maxOfTwo.py"
    assert target.exists()

    module_name = f"student_mod_{abs(hash(str(target)))}"
    _load_module_from_path(module_name, target)

    out = capsys.readouterr().out
    expected = "max=10\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_placeholder_left_in_source():
    target = Path(__file__).resolve().parent / "01_basicTernary_maxOfTwo.py"
    if not target.exists():
        target = Path.cwd() / "01_basicTernary_maxOfTwo.py"
    assert target.exists()

    src = target.read_text(encoding="utf-8")
    assert "________________" not in src, "expected placeholder absent actual present"