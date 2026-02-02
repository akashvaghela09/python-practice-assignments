import importlib.util
import pathlib
import pytest


ASSIGNMENT_FILE = "05_inputUntilQuit.py"


def _load_module_with_name(module_name: str):
    path = pathlib.Path(__file__).resolve().parent / ASSIGNMENT_FILE
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _run_script(monkeypatch, inputs):
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration as e:
            raise AssertionError("expected vs actual: expected more inputs vs actual exhausted") from e

    monkeypatch.setattr("builtins.input", fake_input)

    mod_name = f"student_{abs(hash(tuple(inputs)))}"
    _load_module_with_name(mod_name)


def test_runs_without_syntax_errors(monkeypatch, capsys):
    try:
        _run_script(monkeypatch, ["quit"])
    except SyntaxError as e:
        pytest.fail(f"expected vs actual: expected no SyntaxError vs actual {e}")
    except Exception as e:
        pytest.fail(f"expected vs actual: expected clean run vs actual {type(e).__name__}: {e}")

    out = capsys.readouterr().out.strip()
    assert out != "", "expected vs actual: expected some output vs actual empty"


@pytest.mark.parametrize(
    "inputs, expected_count",
    [
        (["quit"], 0),
        (["hello", "quit"], 1),
        (["hello", "world", "quit"], 2),
        (["a", "b", "c", "quit"], 3),
        (["", "quit"], 1),
        (["   ", "quit"], 1),
        (["quit", "quit"], 0),
    ],
)
def test_counts_non_quit_lines(monkeypatch, capsys, inputs, expected_count):
    _run_script(monkeypatch, inputs)
    out = capsys.readouterr().out.strip()
    expected = f"You entered {expected_count} lines"
    assert out == expected, f"expected vs actual: expected {expected!r} vs actual {out!r}"


def test_quit_is_case_sensitive(monkeypatch, capsys):
    inputs = ["Quit", "quit"]
    _run_script(monkeypatch, inputs)
    out = capsys.readouterr().out.strip()
    expected = "You entered 1 lines"
    assert out == expected, f"expected vs actual: expected {expected!r} vs actual {out!r}"


def test_output_format_exact_spacing(monkeypatch, capsys):
    _run_script(monkeypatch, ["x", "y", "quit"])
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip() != ""]
    assert len(lines) == 1, f"expected vs actual: expected single output line vs actual {len(lines)} lines"
    expected = "You entered 2 lines"
    actual = lines[0].strip()
    assert actual == expected, f"expected vs actual: expected {expected!r} vs actual {actual!r}"