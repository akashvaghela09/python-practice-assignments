import importlib.util
import os
import sys


def _run_module_capture_output(module_filename):
    module_path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_module_05", module_path)
    mod = importlib.util.module_from_spec(spec)

    captured = []

    class _Cap:
        def write(self, s):
            captured.append(s)

        def flush(self):
            pass

    old_stdout = sys.stdout
    try:
        sys.stdout = _Cap()
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old_stdout

    out = "".join(captured)
    return mod, out


def test_output_lines_bytes_and_bytearray():
    _, out = _run_module_capture_output("05_bytesVsBytearray.py")
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]

    expected = ["bytes error: TypeError", "bytearray after: bytearray(b'jello')"]
    assert len(lines) == len(expected), f"expected={len(expected)} actual={len(lines)}"

    for exp, act in zip(expected, lines):
        assert act == exp, f"expected={exp!r} actual={act!r}"


def test_bytearray_mutated_to_jello():
    mod, _ = _run_module_capture_output("05_bytesVsBytearray.py")
    assert hasattr(mod, "ba"), "expected=True actual=False"
    assert isinstance(mod.ba, bytearray), f"expected={bytearray} actual={type(mod.ba)}"
    assert bytes(mod.ba) == b"jello", f"expected={b'jello'!r} actual={bytes(mod.ba)!r}"


def test_bytes_remains_hello():
    mod, _ = _run_module_capture_output("05_bytesVsBytearray.py")
    assert hasattr(mod, "b"), "expected=True actual=False"
    assert isinstance(mod.b, (bytes,)), f"expected={bytes} actual={type(mod.b)}"
    assert mod.b == b"hello", f"expected={b'hello'!r} actual={mod.b!r}"