import importlib
import sys
import types
import pytest


MODULE_NAME = "15_enumerateRunLengthEncoding"


def _exec_module_capture_stdout(monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(map(str, args)) + end)

    monkeypatch.setattr("builtins.print", fake_print)

    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]

    importlib.import_module(MODULE_NAME)
    out = "".join(captured)
    return out


def test_runs_and_output_matches_expected(monkeypatch):
    out = _exec_module_capture_stdout(monkeypatch)
    expected = "a3b1c4a2\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_single_line(monkeypatch):
    out = _exec_module_capture_stdout(monkeypatch)
    expected_lines = 1
    actual_lines = len(out.splitlines())
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_no_extra_whitespace(monkeypatch):
    out = _exec_module_capture_stdout(monkeypatch)
    expected = out.strip()
    actual = out.rstrip("\n")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_module_exposes_expected_globals(monkeypatch):
    if MODULE_NAME in sys.modules:
        del sys.modules[MODULE_NAME]
    mod = importlib.import_module(MODULE_NAME)

    assert isinstance(getattr(mod, "s", None), str)
    assert getattr(mod, "s") == "aaabccccaa"

    parts = getattr(mod, "parts", None)
    assert isinstance(parts, list)

    expected_parts = ["a3", "b1", "c4", "a2"]
    assert parts == expected_parts, f"expected={expected_parts!r} actual={parts!r}"


def test_parts_join_equals_printed_content(monkeypatch):
    out = _exec_module_capture_stdout(monkeypatch)

    if MODULE_NAME in sys.modules:
        mod = sys.modules[MODULE_NAME]
    else:
        mod = importlib.import_module(MODULE_NAME)

    expected = "".join(mod.parts) + "\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_placeholder_tokens_left_in_source():
    import pathlib

    p = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    src = p.read_text(encoding="utf-8")

    expected = False
    actual = "___" in src
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_enumerate_in_source():
    import pathlib

    p = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    src = p.read_text(encoding="utf-8")

    expected = True
    actual = "enumerate(" in src
    assert actual == expected, f"expected={expected!r} actual={actual!r}"