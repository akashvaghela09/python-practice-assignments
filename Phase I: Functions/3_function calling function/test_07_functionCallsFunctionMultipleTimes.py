import importlib
import pytest

MODULE_NAME = "07_functionCallsFunctionMultipleTimes"


def load_module():
    return importlib.import_module(MODULE_NAME)


def test_repeat_char_basic_cases(capsys):
    mod = load_module()
    _ = capsys.readouterr()
    cases = [
        ("a", 0, ""),
        ("a", 1, "a"),
        ("a", 5, "aaaaa"),
        ("-", 4, "----"),
        ("+", 3, "+++"),
        ("xy", 3, "xyxyxy"),
        ("", 10, ""),
    ]
    for ch, times, expected in cases:
        actual = mod.repeat_char(ch, times)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_repeat_char_negative_times(capsys):
    mod = load_module()
    _ = capsys.readouterr()
    expected = ""
    actual = mod.repeat_char("a", -3)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_box_line_formats_correctly(capsys):
    mod = load_module()
    _ = capsys.readouterr()
    cases = [
        (0, "++"),
        (1, "+-+"),
        (4, "+----+"),
        (10, "+----------+"),
    ]
    for width, expected in cases:
        actual = mod.box_line(width)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_box_line_calls_repeat_char(monkeypatch, capsys):
    mod = load_module()
    _ = capsys.readouterr()

    calls = []

    def fake_repeat_char(ch, times):
        calls.append((ch, times))
        return "X" * max(0, int(times))

    monkeypatch.setattr(mod, "repeat_char", fake_repeat_char)

    width = 6
    actual = mod.box_line(width)

    assert calls == [("-", width)], f"expected={[('-', width)]!r} actual={calls!r}"
    expected = "+" + ("X" * width) + "+"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_module_prints_box_line_4(capsys):
    importlib.invalidate_caches()
    if MODULE_NAME in importlib.sys.modules:
        del importlib.sys.modules[MODULE_NAME]
    importlib.import_module(MODULE_NAME)
    out = capsys.readouterr().out
    expected = "+----+\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"