import importlib.util
from pathlib import Path

def _run_script_with_inputs(path, monkeypatch, inputs):
    import builtins
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise AssertionError("expected output\nYou entered 2 lines\nactual output\n<program requested more input>")

    monkeypatch.setattr(builtins, "input", fake_input)

    spec = importlib.util.spec_from_file_location("student_module", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_input_until_quit_counts_lines(capsys, monkeypatch):
    path = Path(__file__).resolve().parent / "05_inputUntilQuit.py"
    if not path.exists():
        raise AssertionError("expected output\nYou entered 2 lines\nactual output\n<missing file>")

    _run_script_with_inputs(path, monkeypatch, ["hello", "world", "quit"])
    out = capsys.readouterr().out
    expected = "You entered 2 lines\n"
    if out != expected:
        raise AssertionError(f"expected output\n{expected}actual output\n{out}")
