import importlib
import contextlib
import io
import sys


def run_module_capture(name: str):
    if name in sys.modules:
        del sys.modules[name]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(name)
    return buf.getvalue()


def test_prints_first_forbidden_character_exactly():
    out = run_module_capture("05_find_first_forbidden_character")
    assert out == "forbidden: '#'\n", f"expected={repr(\"forbidden: '#'\")}, actual={repr(out)}"


def test_prints_single_line_only():
    out = run_module_capture("05_find_first_forbidden_character")
    lines = out.splitlines(True)
    assert len(lines) == 1, f"expected={1}, actual={len(lines)}"
    assert lines[0].endswith("\n"), f"expected={repr(True)}, actual={repr(lines[0].endswith(chr(10)))}"