import ast
import importlib.util
import pathlib
import pytest


FILE_NAME = "01_rangeToListBasics.py"


def load_module_from_path(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("mod_under_test", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_file_has_no_placeholders():
    path = pathlib.Path(__file__).with_name(FILE_NAME)
    content = path.read_text(encoding="utf-8")
    assert "_____" not in content, f"Expected no placeholders, got placeholders present"


def test_nums_is_correct_list(capsys):
    path = pathlib.Path(__file__).with_name(FILE_NAME)
    module = load_module_from_path(path)
    expected = [0, 1, 2, 3, 4]
    actual = getattr(module, "nums", None)
    assert actual == expected, f"Expected {expected}, got {actual}"
    out = capsys.readouterr().out.strip().splitlines()
    assert out, f"Expected {expected}, got {out}"
    assert out[-1].strip() == str(expected), f"Expected {str(expected)}, got {out[-1].strip()}"


def test_uses_list_and_range_calls():
    path = pathlib.Path(__file__).with_name(FILE_NAME)
    tree = ast.parse(path.read_text(encoding="utf-8"))

    assign_nodes = [
        n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "nums" for t in n.targets)
    ]
    assert assign_nodes, "Expected assignment to nums, got none"

    value = assign_nodes[0].value
    assert isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "list", (
        f"Expected list(...) call, got {ast.dump(value, include_attributes=False)}"
    )

    assert value.args, f"Expected list(...) to have arguments, got {ast.dump(value, include_attributes=False)}"
    inner = value.args[0]
    assert isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name) and inner.func.id == "range", (
        f"Expected range(...) inside list(...), got {ast.dump(inner, include_attributes=False)}"
    )

    assert 1 <= len(inner.args) <= 2, f"Expected range with 1 or 2 args, got {len(inner.args)}"


def test_no_extra_output_lines(capsys):
    path = pathlib.Path(__file__).with_name(FILE_NAME)
    load_module_from_path(path)
    out = [line for line in capsys.readouterr().out.splitlines() if line.strip() != ""]
    expected_lines = 1
    actual_lines = len(out)
    assert actual_lines == expected_lines, f"Expected {expected_lines}, got {actual_lines}"