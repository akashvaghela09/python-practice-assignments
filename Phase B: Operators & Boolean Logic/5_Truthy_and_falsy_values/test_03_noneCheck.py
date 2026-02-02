import importlib.util
import os
import sys


def test_output_no_value(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_noneCheck.py")
    spec = importlib.util.spec_from_file_location("nonecheck03", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    expected = "NO VALUE\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"