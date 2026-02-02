import importlib.util
from pathlib import Path

def _run_script_with_inputs(path, monkeypatch, inputs, expected_for_errors):
    import builtins
    it = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise AssertionError(f"expected output\n{expected_for_errors}actual output\n<program requested more input>")

    monkeypatch.setattr(builtins, "input", fake_input)

    spec = importlib.util.spec_from_file_location("student_module", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_password_access_granted_on_third_try(capsys, monkeypatch):
    path = Path(__file__).resolve().parent / "06_passwordAttempts.py"
    if not path.exists():
        raise AssertionError("expected output\nAccess granted\nactual output\n<missing file>")

    _run_script_with_inputs(path, monkeypatch, ["a", "b", "secret"], "Access granted\n")
    out = capsys.readouterr().out
    expected = "Access granted\n"
    if out != expected:
        raise AssertionError(f"expected output\n{expected}actual output\n{out}")


def test_password_access_denied_after_three_failures(capsys, monkeypatch):
    path = Path(__file__).resolve().parent / "06_passwordAttempts.py"
    if not path.exists():
        raise AssertionError("expected output\nAccess denied\nactual output\n<missing file>")

    _run_script_with_inputs(path, monkeypatch, ["x", "y", "z"], "Access denied\n")
    out = capsys.readouterr().out
    expected = "Access denied\n"
    if out != expected:
        raise AssertionError(f"expected output\n{expected}actual output\n{out}")
