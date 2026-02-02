import importlib
import sys


def run_module_capture(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    importlib.invalidate_caches()
    module = importlib.import_module(module_name)
    out = getattr(sys, "stdout").getvalue() if hasattr(sys.stdout, "getvalue") else None
    return module, out


def test_output_lines(capsys):
    if "09_unpackWithEnumerate" in sys.modules:
        del sys.modules["09_unpackWithEnumerate"]
    importlib.invalidate_caches()
    importlib.import_module("09_unpackWithEnumerate")
    captured = capsys.readouterr()
    expected = "1: Ada\n2: Linus\n3: Grace\n"
    actual = captured.out
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_lines_variable_matches_expected(capsys):
    if "09_unpackWithEnumerate" in sys.modules:
        del sys.modules["09_unpackWithEnumerate"]
    importlib.invalidate_caches()
    mod = importlib.import_module("09_unpackWithEnumerate")
    expected = ["1: Ada", "2: Linus", "3: Grace"]
    actual = getattr(mod, "lines", None)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_enumerate(monkeypatch, capsys):
    if "09_unpackWithEnumerate" in sys.modules:
        del sys.modules["09_unpackWithEnumerate"]
    importlib.invalidate_caches()

    calls = []
    import builtins

    real_enumerate = builtins.enumerate

    def spy_enumerate(iterable, start=0):
        calls.append((iterable, start))
        return real_enumerate(iterable, start=start)

    monkeypatch.setattr(builtins, "enumerate", spy_enumerate)

    importlib.import_module("09_unpackWithEnumerate")
    capsys.readouterr()

    expected = 1
    actual = len(calls)
    assert actual >= expected, f"expected>={expected!r} actual={actual!r}"

    exp_start = 1
    got_start = calls[-1][1] if calls else None
    assert got_start == exp_start, f"expected={exp_start!r} actual={got_start!r}"