import sys
import importlib.util
from pathlib import Path
import pytest


def _run_script(script_path: Path, input_data: str = ""):
    if not script_path.exists():
        raise FileNotFoundError(f"Missing assignment file: {script_path}")

    original_stdin = sys.stdin
    original_stdout = sys.stdout

    class _In:
        def __init__(self, s: str):
            self._s = s
            self._i = 0

        def read(self, n=-1):
            if n is None or n < 0:
                out = self._s[self._i :]
                self._i = len(self._s)
                return out
            out = self._s[self._i : self._i + n]
            self._i += n
            return out

        def readline(self):
            if self._i >= len(self._s):
                return ""
            j = self._s.find("\n", self._i)
            if j == -1:
                out = self._s[self._i :]
                self._i = len(self._s)
                return out
            out = self._s[self._i : j + 1]
            self._i = j + 1
            return out

    class _Out:
        def __init__(self):
            self.parts = []

        def write(self, s):
            self.parts.append(s)

        def flush(self):
            pass

        def get(self):
            return "".join(self.parts)

    sys.stdin = _In(input_data)
    out = _Out()
    sys.stdout = out

    try:
        spec = importlib.util.spec_from_file_location(script_path.stem, str(script_path))
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except SystemExit:
            pass
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    return out.get()


def test_prints_1_to_5_exactly():
    script = Path(__file__).resolve().parent / "02_printOneToFive.py"
    expected = "1\n2\n3\n4\n5\n"
    actual = _run_script(script)
    if actual != expected:
        pytest.fail("expected output:\n" + expected + "\nactual output:\n" + actual)
