import importlib.util
import pathlib
import sys
import types
import pytest


FILE_NAME = "10_traceLoopState.py"


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location("trace_loop_state_mod", str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_trace_output_exact(capsys):
    _load_module()
    captured = capsys.readouterr()
    out_lines = captured.out.splitlines()
    expected = [
        "i=0 before=1 after=1",
        "i=1 before=1 after=2",
        "i=2 before=2 after=6",
        "i=3 before=6 after=24",
        "final: 24",
    ]
    assert out_lines == expected, f"expected={expected!r} actual={out_lines!r}"


def test_no_stderr(capsys):
    _load_module()
    captured = capsys.readouterr()
    assert captured.err == "", f"expected={''!r} actual={captured.err!r}"


def test_is_not_importable_by_number_name():
    with pytest.raises(Exception):
        __import__("10_traceLoopState")