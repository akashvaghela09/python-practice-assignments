import importlib
import sys
import types
import pytest


def run_module_capture_stdout(module_name, monkeypatch):
    out = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join("" if a is None else str(a) for a in args) + end
        out.append(s)

    monkeypatch.setattr("builtins.print", fake_print)
    sys.modules.pop(module_name, None)
    importlib.import_module(module_name)
    return "".join(out)


def test_outputs_expected_lines(monkeypatch):
    actual = run_module_capture_stdout("07_skipWithContinue", monkeypatch)
    expected = "1\n2\n3\n5\n6\n7\n"
    assert expected == actual


def test_outputs_only_integers_each_line(monkeypatch):
    actual = run_module_capture_stdout("07_skipWithContinue", monkeypatch)
    lines = actual.splitlines()
    assert lines == [str(int(x)) for x in lines]


def test_outputs_six_lines(monkeypatch):
    actual = run_module_capture_stdout("07_skipWithContinue", monkeypatch)
    assert len(actual.splitlines()) == 6


def test_does_not_print_4(monkeypatch):
    actual = run_module_capture_stdout("07_skipWithContinue", monkeypatch)
    assert "4\n" not in actual


def test_is_increasing_order(monkeypatch):
    actual = run_module_capture_stdout("07_skipWithContinue", monkeypatch)
    nums = [int(x) for x in actual.splitlines()]
    assert nums == sorted(nums)