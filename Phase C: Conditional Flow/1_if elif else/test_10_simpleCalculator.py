import importlib.util
import pathlib


def load_module():
    path = pathlib.Path(__file__).resolve().parent / "10_simpleCalculator.py"
    spec = importlib.util.spec_from_file_location("simpleCalculator10", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_divide_by_zero_message(capsys):
    load_module()
    out = capsys.readouterr().out.strip()
    assert out == "Cannot divide by zero", f"expected={'Cannot divide by zero'} actual={out!r}"


def test_message_not_empty(capsys):
    load_module()
    out = capsys.readouterr().out.strip()
    assert out != "", f"expected={'non-empty output'} actual={out!r}"


def test_no_result_prefix_on_error(capsys):
    load_module()
    out = capsys.readouterr().out.strip()
    assert not out.startswith("Result:"), f"expected={'not starting with Result:'} actual={out!r}"