import importlib.util
import pathlib
import sys


def _load_module():
    path = pathlib.Path(__file__).with_name("10_primeCounter.py")
    name = "primeCounter10"
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_is_valid_python():
    path = pathlib.Path(__file__).with_name("10_primeCounter.py")
    src = path.read_text(encoding="utf-8")
    compile(src, str(path), "exec")


def test_prints_expected_prime_count(capsys):
    _load_module()
    out = capsys.readouterr().out.strip()
    expected = "5"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prime_count_variable_matches_printed_output(capsys):
    m = _load_module()
    out = capsys.readouterr().out.strip()
    expected = "5"
    assert getattr(m, "prime_count", None) == 5, f"expected={5!r} actual={getattr(m, 'prime_count', None)!r}"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_nums_list_unchanged():
    m = _load_module()
    expected = [2, 3, 4, 5, 9, 11, 12, 13]
    assert getattr(m, "nums", None) == expected, f"expected={expected!r} actual={getattr(m, 'nums', None)!r}"


def test_prime_count_is_int_and_nonnegative():
    m = _load_module()
    pc = getattr(m, "prime_count", None)
    assert isinstance(pc, int), f"expected={int!r} actual={type(pc)!r}"
    assert pc >= 0, f"expected={'>= 0'!r} actual={pc!r}"