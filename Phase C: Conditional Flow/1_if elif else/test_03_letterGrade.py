import importlib.util
import os
import sys
import pytest

FILE_NAME = "03_letterGrade.py"


def _run_script_and_capture_stdout(monkeypatch):
    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        s = sep.join(str(a) for a in args) + end
        captured.append(s)

    monkeypatch.setattr("builtins.print", fake_print)

    spec = importlib.util.spec_from_file_location("lettergrade_mod", os.path.join(os.getcwd(), FILE_NAME))
    module = importlib.util.module_from_spec(spec)
    sys.modules["lettergrade_mod"] = module
    spec.loader.exec_module(module)
    out = "".join(captured)
    return module, out


def _expected_grade(score):
    if 90 <= score <= 100:
        return "A"
    if 80 <= score <= 89:
        return "B"
    if 70 <= score <= 79:
        return "C"
    if 60 <= score <= 69:
        return "D"
    return "F"


def _extract_grade_from_output(out):
    text = out.strip()
    if not text:
        return None
    tokens = [t for t in text.split() if t.strip()]
    if not tokens:
        return None
    return tokens[-1]


def test_prints_one_letter_grade_for_default_score(monkeypatch):
    module, out = _run_script_and_capture_stdout(monkeypatch)

    assert hasattr(module, "score")
    expected = _expected_grade(module.score)

    actual = _extract_grade_from_output(out)
    if actual != expected:
        pytest.fail(f"expected={expected!r} actual={actual!r}")

    stripped = out.strip()
    if stripped != expected:
        pytest.fail(f"expected={expected!r} actual={stripped!r}")


def test_prints_exactly_one_line(monkeypatch):
    _, out = _run_script_and_capture_stdout(monkeypatch)
    lines = out.splitlines()
    expected_lines = 1
    actual_lines = len(lines)
    if actual_lines != expected_lines:
        pytest.fail(f"expected={expected_lines!r} actual={actual_lines!r}")


@pytest.mark.parametrize(
    "score, expected",
    [
        (0, "F"),
        (59, "F"),
        (60, "D"),
        (69, "D"),
        (70, "C"),
        (79, "C"),
        (80, "B"),
        (89, "B"),
        (90, "A"),
        (100, "A"),
    ],
)
def test_grading_boundaries_via_patched_score(monkeypatch, score, expected):
    source_path = os.path.join(os.getcwd(), FILE_NAME)
    with open(source_path, "r", encoding="utf-8") as f:
        source = f.read()

    patched = source.replace("score = 83", f"score = {score}", 1)

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)

    mod_name = f"lettergrade_mod_{score}"
    spec = importlib.util.spec_from_loader(mod_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    exec(compile(patched, FILE_NAME, "exec"), module.__dict__)

    out = "".join(captured).strip()
    actual = _extract_grade_from_output(out)
    if actual != expected:
        pytest.fail(f"expected={expected!r} actual={actual!r}")
    if out != expected:
        pytest.fail(f"expected={expected!r} actual={out!r}")