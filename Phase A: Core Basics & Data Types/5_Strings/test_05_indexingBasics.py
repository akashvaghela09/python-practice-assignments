import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("target_module", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_prints_first_and_last_char():
    out = _run_module_capture_stdout("05_indexingBasics.py")
    lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    assert lines, f"expected non-empty output vs actual {out!r}"
    assert lines[-1] == "p n", f"expected {'p n'!r} vs actual {lines[-1]!r}"


def test_no_extra_output_lines():
    out = _run_module_capture_stdout("05_indexingBasics.py")
    lines = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 1, f"expected {1!r} vs actual {len(lines)!r}"


def test_spacing_exact():
    out = _run_module_capture_stdout("05_indexingBasics.py")
    line = [line.rstrip("\n") for line in out.splitlines() if line.strip() != ""][-1]
    assert line.count(" ") == 1, f"expected {1!r} vs actual {line.count(' ')!r}"
    assert line.split(" ") == ["p", "n"], f"expected {['p','n']!r} vs actual {line.split(' ')!r}"