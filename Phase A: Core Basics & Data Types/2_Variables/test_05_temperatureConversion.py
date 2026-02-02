import importlib.util
import pathlib
import sys
import re
import types
import pytest


FILE_NAME = "05_temperatureConversion.py"


def load_module_fresh(tmp_name="tempconv_mod"):
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(tmp_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[tmp_name] = module
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout(monkeypatch):
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    code = path.read_text(encoding="utf-8")

    out = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        out.append(sep.join(str(a) for a in args) + end)

    g = {"__name__": "__main__", "__file__": str(path), "print": fake_print}
    exec(compile(code, str(path), "exec"), g, g)
    return "".join(out)


def compute_expected_from_source():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    src = path.read_text(encoding="utf-8")
    m = re.search(r"^\s*celsius\s*=\s*([+-]?\d+(?:\.\d+)?)\s*$", src, re.MULTILINE)
    assert m is not None
    c = float(m.group(1))
    f = c * 9 / 5 + 32
    if c.is_integer():
        c_str = str(int(c))
    else:
        c_str = str(c)
    return f"{c_str}C is {f}F\n", c, f


def assert_eq_expected(actual, expected):
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_runs_and_prints_single_line(monkeypatch):
    expected, _, _ = compute_expected_from_source()
    actual = run_script_capture_stdout(monkeypatch)
    assert_eq_expected(actual, expected)


def test_module_has_celsius_and_fahrenheit_and_types():
    mod = load_module_fresh("tempconv_mod_a")
    assert hasattr(mod, "celsius")
    assert hasattr(mod, "fahrenheit")
    assert isinstance(mod.celsius, (int, float))
    assert isinstance(mod.fahrenheit, (int, float))


def test_fahrenheit_matches_formula():
    _, c, f_expected = compute_expected_from_source()
    mod = load_module_fresh("tempconv_mod_b")
    actual = float(mod.fahrenheit)
    expected = float(f_expected)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_printed_line_matches_module_values(monkeypatch):
    mod = load_module_fresh("tempconv_mod_c")
    actual_out = run_script_capture_stdout(monkeypatch)

    c = mod.celsius
    f = mod.fahrenheit
    expected_out = f"{c}C is {f}F\n"
    assert_eq_expected(actual_out, expected_out)