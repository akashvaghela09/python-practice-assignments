import builtins
import importlib.util
import sys
from pathlib import Path
import pytest


ASSIGNMENT_FILE = "11_runningTotalThreeInputs.py"


def load_module_from_path(tmp_path, monkeypatch, inputs):
    src = Path(__file__).resolve().parent / ASSIGNMENT_FILE
    if not src.exists():
        src = Path(ASSIGNMENT_FILE).resolve()
    assert src.exists()

    dst = tmp_path / ASSIGNMENT_FILE
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    it = iter([str(x) for x in inputs])

    def fake_input(prompt=""):
        return next(it)

    monkeypatch.setattr(builtins, "input", fake_input)

    mod_name = f"student_mod_{hash(tuple(inputs))}_{dst.stat().st_mtime_ns}"
    spec = importlib.util.spec_from_file_location(mod_name, str(dst))
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def run_case(tmp_path, monkeypatch, capsys, inputs):
    load_module_from_path(tmp_path, monkeypatch, inputs)
    out = capsys.readouterr().out
    return out


@pytest.mark.parametrize(
    "inputs",
    [
        (4, 1, 9),
        (0, 0, 0),
        (-1, 2, -3),
        (100000, 200000, 300000),
    ],
)
def test_running_total_output_format_and_value(tmp_path, monkeypatch, capsys, inputs):
    out = run_case(tmp_path, monkeypatch, capsys, inputs)

    expected_total = sum(inputs)
    expected = f"total={expected_total}\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_prints_exactly_one_line(tmp_path, monkeypatch, capsys):
    inputs = (7, 8, 9)
    out = run_case(tmp_path, monkeypatch, capsys, inputs)

    lines = out.splitlines(True)
    expected_total = sum(inputs)
    expected = f"total={expected_total}\n"
    assert len(lines) == 1 and out == expected, f"expected={expected!r} actual={out!r}"


def test_uses_all_three_inputs(tmp_path, monkeypatch, capsys):
    inputs = (1, 10, 100)
    out = run_case(tmp_path, monkeypatch, capsys, inputs)

    expected_total = sum(inputs)
    expected = f"total={expected_total}\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"