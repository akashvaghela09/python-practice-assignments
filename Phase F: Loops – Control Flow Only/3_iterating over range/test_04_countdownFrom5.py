import importlib.util
import pathlib
import re

def _run_script_capture_stdout(script_path, capsys):
    spec = importlib.util.spec_from_file_location("student_module_04", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return out

def test_countdown_output_exact(capsys):
    script_path = pathlib.Path(__file__).resolve().parent / "04_countdownFrom5.py"
    out = _run_script_capture_stdout(str(script_path), capsys)
    actual_lines = [line.rstrip("\n") for line in out.splitlines()]
    expected_lines = ["5", "4", "3", "2", "1"]
    assert actual_lines == expected_lines, f"expected={expected_lines} actual={actual_lines}"

def test_no_extra_whitespace_in_lines(capsys):
    script_path = pathlib.Path(__file__).resolve().parent / "04_countdownFrom5.py"
    out = _run_script_capture_stdout(str(script_path), capsys)
    actual_lines = out.splitlines()
    stripped = [s.strip() for s in actual_lines]
    assert actual_lines == stripped, f"expected={stripped} actual={actual_lines}"

def test_prints_only_integers_5_to_1_once_each(capsys):
    script_path = pathlib.Path(__file__).resolve().parent / "04_countdownFrom5.py"
    out = _run_script_capture_stdout(str(script_path), capsys)
    nums = []
    for line in out.splitlines():
        if re.fullmatch(r"-?\d+", line.strip()):
            nums.append(int(line.strip()))
        else:
            nums.append(None)
    expected = [5, 4, 3, 2, 1]
    assert nums == expected, f"expected={expected} actual={nums}"