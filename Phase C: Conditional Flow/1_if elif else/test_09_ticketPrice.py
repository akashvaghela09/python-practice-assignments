import importlib.util
import sys
from pathlib import Path


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_script_capture_stdout(monkeypatch, tmp_path, age, show_time):
    src = Path(__file__).resolve().parent / "09_ticketPrice.py"
    code = src.read_text(encoding="utf-8")

    injected = (
        f"age = {age}\n"
        f"show_time = {show_time!r}\n"
        + code
    )

    test_file = tmp_path / "09_ticketPrice_exec.py"
    test_file.write_text(injected, encoding="utf-8")

    out = []
    monkeypatch.setattr("builtins.print", lambda *a, **k: out.append(" ".join(map(str, a))))
    load_module_from_path("ticket_price_exec_mod", test_file)
    return out


def assert_single_line_output(lines, expected):
    got = "\n".join(lines)
    assert got == expected, f"expected={expected!r} actual={got!r}"


def test_expected_example_age70_matinee(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 70, "matinee")
    assert_single_line_output(lines, "Ticket price: 7")


def test_invalid_age_negative(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, -1, "matinee")
    assert_single_line_output(lines, "Invalid age")


def test_child_matinee(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 10, "matinee")
    assert_single_line_output(lines, "Ticket price: 6")


def test_child_evening(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 12, "evening")
    assert_single_line_output(lines, "Ticket price: 8")


def test_adult_evening(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 30, "evening")
    assert_single_line_output(lines, "Ticket price: 12")


def test_adult_matinee(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 64, "matinee")
    assert_single_line_output(lines, "Ticket price: 10")


def test_senior_evening(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 65, "evening")
    assert_single_line_output(lines, "Ticket price: 9")


def test_invalid_show_time_no_price(monkeypatch, tmp_path):
    lines = run_script_capture_stdout(monkeypatch, tmp_path, 30, "midnight")
    assert_single_line_output(lines, "Invalid show time")