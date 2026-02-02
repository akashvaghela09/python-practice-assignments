import importlib.util
import pathlib
import sys
import types
import builtins
import pytest


def _load_module_with_capture(path):
    outputs = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        outputs.append(s)

    module_name = f"student_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)

    real_print = builtins.print
    builtins.print = fake_print
    try:
        spec.loader.exec_module(module)
    finally:
        builtins.print = real_print

    return module, outputs


def _expected_sum_1_to_n(n):
    return sum(range(1, n + 1))


@pytest.fixture(scope="module")
def mod_and_out():
    path = pathlib.Path(__file__).with_name("02_sumFirstN.py")
    return _load_module_with_capture(path)


def test_module_runs_and_prints_once(mod_and_out):
    _, out = mod_and_out
    printed = "".join(out).strip().splitlines()
    assert len(printed) == 1


def test_printed_value_is_correct_for_default_n(mod_and_out):
    mod, out = mod_and_out
    expected = _expected_sum_1_to_n(getattr(mod, "n"))
    actual_line = "".join(out).strip().splitlines()[0]
    actual = int(actual_line)
    assert expected == actual, f"expected={expected} actual={actual}"


def test_total_variable_matches_expected(mod_and_out):
    mod, _ = mod_and_out
    expected = _expected_sum_1_to_n(getattr(mod, "n"))
    actual = getattr(mod, "total")
    assert expected == actual, f"expected={expected} actual={actual}"


def test_source_uses_for_loop_and_range():
    path = pathlib.Path(__file__).with_name("02_sumFirstN.py")
    src = path.read_text(encoding="utf-8")
    assert "for " in src
    assert "range" in src


def test_no_input_call_used():
    path = pathlib.Path(__file__).with_name("02_sumFirstN.py")
    src = path.read_text(encoding="utf-8")
    assert "input(" not in src