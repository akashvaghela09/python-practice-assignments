import importlib
import sys
import pytest

MODULE_NAME = "04_avoidingAliasingCopy"


def run_main_and_capture_output(capsys):
    mod = importlib.import_module(MODULE_NAME)
    mod.main()
    out = capsys.readouterr().out
    return out


def test_prints_expected_output_exactly(capsys):
    out = run_main_and_capture_output(capsys)
    expected = "original: [1, 2, 3]\ncopy: [1, 2, 3, 99]\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_main_idempotent_output(capsys):
    mod = importlib.import_module(MODULE_NAME)

    mod.main()
    out1 = capsys.readouterr().out

    mod.main()
    out2 = capsys.readouterr().out

    assert out2 == out1, f"expected={out1!r} actual={out2!r}"


def test_module_import_has_no_output(capsys):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    importlib.import_module(MODULE_NAME)
    out = capsys.readouterr().out
    expected = ""
    assert out == expected, f"expected={expected!r} actual={out!r}"