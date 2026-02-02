import importlib.util
import pathlib
import re
import subprocess
import sys


def test_prints_6_0():
    path = pathlib.Path(__file__).resolve().parent / "04_leftToRightWithSamePrecedence.py"
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    assert proc.returncode == 0, f"expected 0, actual {proc.returncode}"
    out = proc.stdout.strip()
    assert out == "6.0", f"expected 6.0, actual {out}"


def test_no_placeholders_left():
    path = pathlib.Path(__file__).resolve().parent / "04_leftToRightWithSamePrecedence.py"
    src = path.read_text(encoding="utf-8")
    placeholders = re.findall(r"\b__\b", src)
    assert len(placeholders) == 0, f"expected 0, actual {len(placeholders)}"


def test_result_is_float_6_0():
    path = pathlib.Path(__file__).resolve().parent / "04_leftToRightWithSamePrecedence.py"
    spec = importlib.util.spec_from_file_location("m04_leftToRightWithSamePrecedence", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert isinstance(module.result, (int, float)), f"expected numeric, actual {type(module.result).__name__}"
    assert float(module.result) == 6.0, f"expected 6.0, actual {float(module.result)}"