import importlib.util
import pathlib
import sys


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_output_filters_by_min_length(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "08_filterWordsByMinLength.py"
    module_name = "assignment_08_filterWordsByMinLength"
    load_module_from_path(module_name, file_path)

    captured = capsys.readouterr()
    actual = captured.out.strip()
    expected = "elephant giraffe"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_no_unexpected_stderr(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "08_filterWordsByMinLength.py"
    module_name = "assignment_08_filterWordsByMinLength_stderr"
    load_module_from_path(module_name, file_path)

    captured = capsys.readouterr()
    actual_err = captured.err
    expected_err = ""
    assert actual_err == expected_err, f"expected={expected_err!r} actual={actual_err!r}"


def test_output_has_single_spaces_and_no_extra_words(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "08_filterWordsByMinLength.py"
    module_name = "assignment_08_filterWordsByMinLength_format"
    load_module_from_path(module_name, file_path)

    out = capsys.readouterr().out.rstrip("\n")
    actual_tokens = out.split(" ") if out else [""]
    expected_tokens = ["elephant", "giraffe"]
    assert actual_tokens == expected_tokens, f"expected={expected_tokens!r} actual={actual_tokens!r}"