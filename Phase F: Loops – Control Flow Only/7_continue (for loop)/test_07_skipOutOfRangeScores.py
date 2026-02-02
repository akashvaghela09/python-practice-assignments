import importlib.util
import os
import re


def _run_module_capture_stdout(module_filename, capsys):
    spec = importlib.util.spec_from_file_location("student_module", module_filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = capsys.readouterr().out
    return mod, out


def test_stdout_exact_value_and_format(capsys):
    module_filename = os.path.join(os.path.dirname(__file__), "07_skipOutOfRangeScores.py")
    _, out = _run_module_capture_stdout(module_filename, capsys)

    lines = [ln for ln in out.splitlines() if ln.strip() != ""]
    assert len(lines) == 1, f"expected={1} actual={len(lines)}"

    line = lines[0].strip()
    assert re.fullmatch(r"-?\d+\.\d{2}", line) is not None, f"expected={'<float with 2 decimals>'} actual={line}"

    expected = "76.67"
    assert line == expected, f"expected={expected} actual={line}"


def test_average_is_based_on_in_range_scores(capsys):
    module_filename = os.path.join(os.path.dirname(__file__), "07_skipOutOfRangeScores.py")
    mod, _ = _run_module_capture_stdout(module_filename, capsys)

    assert hasattr(mod, "scores"), f"expected={'has scores'} actual={'missing'}"
    assert hasattr(mod, "avg"), f"expected={'has avg'} actual={'missing'}"

    expected_avg = sum([s for s in mod.scores if 0 <= s <= 100]) / len([s for s in mod.scores if 0 <= s <= 100])
    actual_avg = mod.avg
    assert abs(actual_avg - expected_avg) < 1e-12, f"expected={expected_avg} actual={actual_avg}"


def test_valid_count_matches_number_of_valid_scores(capsys):
    module_filename = os.path.join(os.path.dirname(__file__), "07_skipOutOfRangeScores.py")
    mod, _ = _run_module_capture_stdout(module_filename, capsys)

    assert hasattr(mod, "valid_count"), f"expected={'has valid_count'} actual={'missing'}"
    expected_count = len([s for s in mod.scores if 0 <= s <= 100])
    actual_count = mod.valid_count
    assert actual_count == expected_count, f"expected={expected_count} actual={actual_count}"


def test_valid_sum_matches_sum_of_valid_scores(capsys):
    module_filename = os.path.join(os.path.dirname(__file__), "07_skipOutOfRangeScores.py")
    mod, _ = _run_module_capture_stdout(module_filename, capsys)

    assert hasattr(mod, "valid_sum"), f"expected={'has valid_sum'} actual={'missing'}"
    expected_sum = sum([s for s in mod.scores if 0 <= s <= 100])
    actual_sum = mod.valid_sum
    assert actual_sum == expected_sum, f"expected={expected_sum} actual={actual_sum}"