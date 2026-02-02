import importlib.util
import pathlib
import sys


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_module_executes_without_syntax_error(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    _load_module("temperatureAlert_06_exec", file_path)
    out = capsys.readouterr().out.strip()
    assert out in {"DANGER", "OK"}, f"expected one of {{'DANGER','OK'}}, got {out!r}"


def test_alert_logic_danger_for_36_75(monkeypatch, capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    src = file_path.read_text(encoding="utf-8")

    src = src.replace("temperature = 36", "temperature = 36")
    src = src.replace("humidity = 75", "humidity = 75")
    monkeypatch.setattr(file_path.__class__, "read_text", lambda self, encoding=None: src)

    _load_module("temperatureAlert_06_case1", file_path)
    out = capsys.readouterr().out.strip()
    expected = "DANGER"
    assert out == expected, f"expected {expected!r}, got {out!r}"


def test_alert_logic_ok_for_34_80(monkeypatch, capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    original = file_path.read_text(encoding="utf-8")

    src = original.replace("temperature = 36", "temperature = 34").replace("humidity = 75", "humidity = 80")
    monkeypatch.setattr(file_path.__class__, "read_text", lambda self, encoding=None: src)

    _load_module("temperatureAlert_06_case2", file_path)
    out = capsys.readouterr().out.strip()
    expected = "OK"
    assert out == expected, f"expected {expected!r}, got {out!r}"


def test_precedence_case_35_70_is_danger(monkeypatch, capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    original = file_path.read_text(encoding="utf-8")

    src = original.replace("temperature = 36", "temperature = 35").replace("humidity = 75", "humidity = 70")
    monkeypatch.setattr(file_path.__class__, "read_text", lambda self, encoding=None: src)

    _load_module("temperatureAlert_06_case3", file_path)
    out = capsys.readouterr().out.strip()
    expected = "DANGER"
    assert out == expected, f"expected {expected!r}, got {out!r}"


def test_precedence_case_39_10_is_ok(monkeypatch, capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    original = file_path.read_text(encoding="utf-8")

    src = original.replace("temperature = 36", "temperature = 39").replace("humidity = 75", "humidity = 10")
    monkeypatch.setattr(file_path.__class__, "read_text", lambda self, encoding=None: src)

    _load_module("temperatureAlert_06_case4", file_path)
    out = capsys.readouterr().out.strip()
    expected = "OK"
    assert out == expected, f"expected {expected!r}, got {out!r}"


def test_temperature_40_is_danger_regardless_of_humidity(monkeypatch, capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "06_temperatureAlert.py"
    original = file_path.read_text(encoding="utf-8")

    src = original.replace("temperature = 36", "temperature = 40").replace("humidity = 75", "humidity = 0")
    monkeypatch.setattr(file_path.__class__, "read_text", lambda self, encoding=None: src)

    _load_module("temperatureAlert_06_case5", file_path)
    out = capsys.readouterr().out.strip()
    expected = "DANGER"
    assert out == expected, f"expected {expected!r}, got {out!r}"