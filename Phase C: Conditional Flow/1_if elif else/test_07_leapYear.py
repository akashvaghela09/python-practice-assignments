import sys
import importlib.util
from pathlib import Path


def _run_script(path: Path, monkeypatch):
    if not path.exists():
        raise AssertionError(f"Missing assignment file: {path}")

    captured = []

    def _fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        captured.append(s)

    monkeypatch.setattr(sys.modules["builtins"], "print", _fake_print)

    spec = importlib.util.spec_from_file_location("mod_07_leapYear", str(path))
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)

    return "".join(captured)


def test_leap_year(monkeypatch):
    path = Path(__file__).resolve().parent / "07_leapYear.py"
    actual = _run_script(path, monkeypatch)
    expected = "Not Leap\n"
    if actual != expected:
        raise AssertionError(f"Expected output:\n{expected}\nActual output:\n{actual}")
