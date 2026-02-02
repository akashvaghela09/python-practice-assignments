import importlib.util
import sys
from pathlib import Path
import pytest


ASSIGNMENT_FILE = "06_passwordAttempts.py"


def load_module_from_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_script_with_inputs(tmp_path, inputs):
    src = Path(__file__).resolve().parent / ASSIGNMENT_FILE
    if not src.exists():
        pytest.fail(f"missing file: expected={ASSIGNMENT_FILE} actual=not found")
    dst = tmp_path / ASSIGNMENT_FILE
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    it = iter(inputs)

    def fake_input(prompt=""):
        return next(it)

    mod_name = f"mod_{ASSIGNMENT_FILE.replace('.','_')}_{abs(hash(tuple(inputs)))}"
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    return dst, mod_name, fake_input


def test_runs_without_placeholders(tmp_path):
    dst, mod_name, fake_input = run_script_with_inputs(tmp_path, ["secret"])
    code = dst.read_text(encoding="utf-8")
    assert "__________" not in code, f"expected=no placeholders actual=placeholders present"
    # Ensure it imports/executes without syntax errors
    load_module_from_path(dst, mod_name)


@pytest.mark.parametrize(
    "inputs, expected_line",
    [
        (["secret"], "Access granted"),
        (["a", "secret"], "Access granted"),
        (["a", "b", "secret"], "Access granted"),
        (["a", "b", "c"], "Access denied"),
        (["wrong", "wrong", "wrong"], "Access denied"),
    ],
)
def test_password_attempts_outcome(tmp_path, monkeypatch, capsys, inputs, expected_line):
    dst, mod_name, fake_input = run_script_with_inputs(tmp_path, inputs)
    monkeypatch.setattr("builtins.input", fake_input)
    load_module_from_path(dst, mod_name)
    out = capsys.readouterr().out.splitlines()
    actual_line = out[-1] if out else ""
    assert actual_line == expected_line, f"expected={expected_line} actual={actual_line}"


def test_stops_after_success_does_not_consume_extra_inputs(tmp_path, monkeypatch, capsys):
    consumed = {"n": 0}

    seq = ["a", "secret", "extra1", "extra2"]
    it = iter(seq)

    def fake_input(prompt=""):
        consumed["n"] += 1
        return next(it)

    src = Path(__file__).resolve().parent / ASSIGNMENT_FILE
    if not src.exists():
        pytest.fail(f"missing file: expected={ASSIGNMENT_FILE} actual=not found")
    dst = tmp_path / ASSIGNMENT_FILE
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    code = dst.read_text(encoding="utf-8")
    assert "__________" not in code, f"expected=no placeholders actual=placeholders present"

    mod_name = f"mod_{ASSIGNMENT_FILE.replace('.','_')}_stop_after_success"
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    monkeypatch.setattr("builtins.input", fake_input)
    load_module_from_path(dst, mod_name)

    out = capsys.readouterr().out.splitlines()
    actual_line = out[-1] if out else ""
    assert actual_line == "Access granted", f"expected=Access granted actual={actual_line}"
    assert consumed["n"] == 2, f"expected=2 actual={consumed['n']}"


def test_exactly_three_attempts_on_failure(tmp_path, monkeypatch, capsys):
    consumed = {"n": 0}
    seq = ["x", "y", "z", "should_not_be_used"]
    it = iter(seq)

    def fake_input(prompt=""):
        consumed["n"] += 1
        return next(it)

    src = Path(__file__).resolve().parent / ASSIGNMENT_FILE
    if not src.exists():
        pytest.fail(f"missing file: expected={ASSIGNMENT_FILE} actual=not found")
    dst = tmp_path / ASSIGNMENT_FILE
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    code = dst.read_text(encoding="utf-8")
    assert "__________" not in code, f"expected=no placeholders actual=placeholders present"

    mod_name = f"mod_{ASSIGNMENT_FILE.replace('.','_')}_three_fail"
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    monkeypatch.setattr("builtins.input", fake_input)
    load_module_from_path(dst, mod_name)

    out = capsys.readouterr().out.splitlines()
    actual_line = out[-1] if out else ""
    assert actual_line == "Access denied", f"expected=Access denied actual={actual_line}"
    assert consumed["n"] == 3, f"expected=3 actual={consumed['n']}"


def test_does_not_print_both_messages(tmp_path, monkeypatch, capsys):
    dst, mod_name, fake_input = run_script_with_inputs(tmp_path, ["a", "b", "secret"])
    monkeypatch.setattr("builtins.input", fake_input)
    load_module_from_path(dst, mod_name)
    out = capsys.readouterr().out.splitlines()
    granted = sum(1 for line in out if line.strip() == "Access granted")
    denied = sum(1 for line in out if line.strip() == "Access denied")
    assert (granted + denied) == 1, f"expected=1 actual={granted + denied}"