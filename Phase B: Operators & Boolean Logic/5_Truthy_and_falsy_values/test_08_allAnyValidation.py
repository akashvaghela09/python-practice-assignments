import importlib.util
import io
import os
import sys


def load_module_from_filename(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_module_08", path)
    module = importlib.util.module_from_spec(spec)
    return spec, module, path


def test_prints_valid_only(capsys):
    filename = "08_allAnyValidation.py"
    spec, module, _ = load_module_from_filename(filename)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    expected = "VALID\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_uses_all_truthiness():
    filename = "08_allAnyValidation.py"
    _, _, path = load_module_from_filename(filename)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    expected_contains = "all("
    actual_contains = expected_contains in src
    assert actual_contains, f"expected={True!r} actual={actual_contains!r}"


def test_has_required_list_defined():
    filename = "08_allAnyValidation.py"
    spec, module, _ = load_module_from_filename(filename)
    spec.loader.exec_module(module)

    expected_type = list
    actual_type = type(getattr(module, "required", None))
    assert actual_type is expected_type, f"expected={expected_type} actual={actual_type}"


def test_required_values_are_nonempty_strings():
    filename = "08_allAnyValidation.py"
    spec, module, _ = load_module_from_filename(filename)
    spec.loader.exec_module(module)

    req = getattr(module, "required", None)
    expected_all_strings = True
    actual_all_strings = isinstance(req, list) and all(isinstance(x, str) for x in req)
    assert actual_all_strings == expected_all_strings, f"expected={expected_all_strings!r} actual={actual_all_strings!r}"

    expected_all_truthy = True
    actual_all_truthy = isinstance(req, list) and all(req)
    assert actual_all_truthy == expected_all_truthy, f"expected={expected_all_truthy!r} actual={actual_all_truthy!r}"