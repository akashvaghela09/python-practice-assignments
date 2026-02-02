import importlib.util
import io
import os
import sys


def _load_module_and_capture_output():
    filename = "01_listCreationAndIndexing.py"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("assignment_01_listCreationAndIndexing", path)
    module = importlib.util.module_from_spec(spec)

    stdout = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = stdout
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old_stdout

    return module, stdout.getvalue()


def test_printed_output_exact():
    _, out = _load_module_and_capture_output()
    expected = "Monday\nSunday\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_weekdays_list_exists_and_is_list():
    module, _ = _load_module_and_capture_output()
    assert hasattr(module, "weekdays")
    assert isinstance(module.weekdays, list)


def test_weekdays_length_and_first_last():
    module, _ = _load_module_and_capture_output()
    assert len(module.weekdays) == 7
    assert module.weekdays[0] == "Monday"
    assert module.weekdays[-1] == "Sunday"


def test_weekdays_contents_unique_and_strings():
    module, _ = _load_module_and_capture_output()
    assert all(isinstance(x, str) for x in module.weekdays)
    assert len(set(module.weekdays)) == 7