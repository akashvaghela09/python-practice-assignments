import importlib.util
import pathlib
import sys


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script_and_capture(path, monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        captured.append(" ".join(str(a) for a in args))

    monkeypatch.setattr("builtins.print", fake_print)
    mod = load_module(path)
    return mod, captured


def test_prints_expected_valid_count(monkeypatch):
    path = pathlib.Path(__file__).with_name("12_validateRequiredKeys.py")
    _, out = run_script_and_capture(path, monkeypatch)

    expected = sum(1 for rec in records_fixture() if required_fixture().issubset(rec.keys()))
    actual = int(out[-1]) if out else None

    assert actual == expected, f"expected={expected} actual={actual}"


def test_valid_count_variable_matches_expected_if_present(monkeypatch):
    path = pathlib.Path(__file__).with_name("12_validateRequiredKeys.py")
    mod, _ = run_script_and_capture(path, monkeypatch)

    expected = sum(1 for rec in records_fixture() if required_fixture().issubset(rec.keys()))
    actual = getattr(mod, "valid_count", None)

    assert actual == expected, f"expected={expected} actual={actual}"


def test_no_invalid_key_assumptions(monkeypatch):
    path = pathlib.Path(__file__).with_name("12_validateRequiredKeys.py")
    mod, _ = run_script_and_capture(path, monkeypatch)

    req = getattr(mod, "required", None)
    recs = getattr(mod, "records", None)

    assert isinstance(req, set), f"expected={set} actual={type(req)}"
    assert isinstance(recs, list), f"expected={list} actual={type(recs)}"

    expected = sum(1 for rec in recs if req.issubset(rec.keys()))
    actual = getattr(mod, "valid_count", None)

    assert actual == expected, f"expected={expected} actual={actual}"


def records_fixture():
    return [
        {"id": 1, "name": "Kai"},
        {"id": 2},
        {"name": "Mina"},
        {"id": 4, "name": "Sol"},
    ]


def required_fixture():
    return {"id", "name"}