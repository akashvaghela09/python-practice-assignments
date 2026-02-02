import importlib.util
import pathlib
import sys
import pytest


def load_module_from_path(path: pathlib.Path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(name, None)
    spec.loader.exec_module(module)
    return module


def test_output_numbers_1_to_5_each_on_new_line(capsys):
    path = pathlib.Path(__file__).resolve().parent / "01_whileCountUp.py"
    try:
        load_module_from_path(path)
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")

    out = capsys.readouterr().out
    expected = "1\n2\n3\n4\n5\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output(capsys):
    path = pathlib.Path(__file__).resolve().parent / "01_whileCountUp.py"
    try:
        load_module_from_path(path)
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")

    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip() != ""]
    expected_lines = ["1", "2", "3", "4", "5"]
    assert lines == expected_lines, f"expected={expected_lines!r} actual={lines!r}"


def test_does_not_hang(monkeypatch):
    path = pathlib.Path(__file__).resolve().parent / "01_whileCountUp.py"

    printed = []
    original_print = print

    def fake_print(*args, **kwargs):
        printed.append(" ".join(map(str, args)))
        if len(printed) > 50:
            raise RuntimeError("too_many_prints")
        return original_print(*args, **kwargs)

    monkeypatch.setattr("builtins.print", fake_print)

    try:
        load_module_from_path(path)
    except RuntimeError as e:
        pytest.fail(f"expected=finite_loop actual=RuntimeError:{str(e)}")
    except SyntaxError as e:
        pytest.fail(f"expected=valid_python actual=SyntaxError:{e.msg}")