import importlib.util
import pathlib
import sys


def test_output_matches_expected(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "11_ternary_in_list_comprehension.py"
    spec = importlib.util.spec_from_file_location("m11_ternary_in_list_comprehension", str(file_path))
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    out = capsys.readouterr().out
    expected = "['O', 'E', 'O', 'E']\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_labels_value_if_present(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "11_ternary_in_list_comprehension.py"
    spec = importlib.util.spec_from_file_location("m11_ternary_in_list_comprehension_labels", str(file_path))
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)
    capsys.readouterr()

    if hasattr(module, "labels"):
        expected = ['O', 'E', 'O', 'E']
        actual = module.labels
        assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_labels_length_if_present(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "11_ternary_in_list_comprehension.py"
    spec = importlib.util.spec_from_file_location("m11_ternary_in_list_comprehension_len", str(file_path))
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)
    capsys.readouterr()

    if hasattr(module, "labels"):
        expected = 4
        actual = len(module.labels)
        assert actual == expected, f"expected={expected!r} actual={actual!r}"