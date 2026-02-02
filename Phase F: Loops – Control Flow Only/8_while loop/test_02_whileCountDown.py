import importlib.util
from pathlib import Path

def _run_script(path, monkeypatch):
    import builtins
    def fake_input(prompt=""):
        raise AssertionError("expected output\n5\n4\n3\n2\n1\nactual output\n<program requested input>")
    monkeypatch.setattr(builtins, "input", fake_input)

    spec = importlib.util.spec_from_file_location("student_module", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_count_down_stdout_exact(capsys, monkeypatch):
    path = Path(__file__).resolve().parent / "02_whileCountDown.py"
    if not path.exists():
        raise AssertionError("expected output\n5\n4\n3\n2\n1\nactual output\n<missing file>")

    _run_script(path, monkeypatch)
    out = capsys.readouterr().out
    expected = "5\n4\n3\n2\n1\n"
    if out != expected:
        raise AssertionError(f"expected output\n{expected}actual output\n{out}")
