import importlib.util
import sys
from pathlib import Path


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_prints_first_index_above_threshold_and_stops(capsys):
    file_path = Path(__file__).resolve().parent / "06_firstAboveThresholdIndex.py"
    module_name = "assignment_06_firstAboveThresholdIndex"
    _load_module(module_name, file_path)

    out = capsys.readouterr().out.strip().splitlines()

    values = [10, 50, 100, 101, 200]
    expected_index = None
    for i, v in enumerate(values):
        if v > 100:
            expected_index = i
            break

    assert len(out) == 1, f"expected={1} actual={len(out)}"
    assert out[0] == str(expected_index), f"expected={str(expected_index)} actual={out[0]}"


def test_output_is_integer_line(capsys):
    file_path = Path(__file__).resolve().parent / "06_firstAboveThresholdIndex.py"
    module_name = "assignment_06_firstAboveThresholdIndex_2"
    _load_module(module_name, file_path)

    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1, f"expected={1} actual={len(out)}"
    line = out[0]
    parsed_ok = True
    try:
        int(line)
    except Exception:
        parsed_ok = False
    assert parsed_ok is True, f"expected={True} actual={parsed_ok}"