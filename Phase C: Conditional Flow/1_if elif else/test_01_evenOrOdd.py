import importlib.util
import io
import os
import sys


def _run_module_capture_stdout(module_filename):
    path = os.path.join(os.path.dirname(__file__), module_filename)
    spec = importlib.util.spec_from_file_location("student_mod", path)
    module = importlib.util.module_from_spec(spec)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        spec.loader.exec_module(module)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return module, output


def test_prints_expected_for_default_n():
    module, out = _run_module_capture_stdout("01_evenOrOdd.py")
    expected = "Odd"
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_prints_even_when_n_is_12(monkeypatch):
    module, _ = _run_module_capture_stdout("01_evenOrOdd.py")
    module.n = 12

    def even_or_odd(val):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            exec(open(os.path.join(os.path.dirname(__file__), "01_evenOrOdd.py"), "r", encoding="utf-8").read(), {"n": val})
        finally:
            sys.stdout = old
        return buf.getvalue().strip()

    expected = "Even"
    actual = even_or_odd(12)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_output_is_exact_single_token_even_or_odd():
    _, out = _run_module_capture_stdout("01_evenOrOdd.py")
    actual = out
    stripped = actual.strip()
    assert stripped in {"Even", "Odd"}, f"expected={'Even or Odd'!r} actual={stripped!r}"
    assert actual.strip() == stripped and "\n\n" not in actual, f"expected={'single line'!r} actual={actual!r}"