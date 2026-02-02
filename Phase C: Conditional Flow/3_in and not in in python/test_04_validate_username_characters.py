import importlib.util
import sys
from pathlib import Path


def _run_script_capture_output(script_path, capsys):
    spec = importlib.util.spec_from_file_location(script_path.stem, str(script_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return out


def test_output_lines_and_order(capsys):
    script_path = Path(__file__).resolve().parent / "04_validate_username_characters.py"
    out = _run_script_capture_output(script_path, capsys)
    lines = [line.rstrip("\n") for line in out.splitlines()]
    assert lines == ["VALID", "INVALID"], f"expected={['VALID','INVALID']} actual={lines}"


def test_no_extra_whitespace_or_output(capsys):
    script_path = Path(__file__).resolve().parent / "04_validate_username_characters.py"
    out = _run_script_capture_output(script_path, capsys)
    assert out == "VALID\nINVALID\n", f"expected={'VALID\\nINVALID\\n'} actual={out}"


def test_allowed_definition_and_usage_present():
    script_path = Path(__file__).resolve().parent / "04_validate_username_characters.py"
    text = script_path.read_text(encoding="utf-8")
    assert 'allowed = "abcdefghijklmnopqrstuvwxyz0123456789_"' in text, "expected=allowed_definition actual=missing_or_changed"
    assert "in allowed" in text, "expected=contains_in_allowed actual=missing"
    assert "not in allowed" in text, "expected=contains_not_in_allowed actual=missing"