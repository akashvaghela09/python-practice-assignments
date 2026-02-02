import importlib.util
import io
import os
import sys


def _load_module_capture_output(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location("student_mod_06", path)
    module = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_stdout_three_lines_exact():
    out = _load_module_capture_output("06_dictAccessAndTypes.py")
    expected = "Ada\n36\n<class 'int'>\n"
    assert expected == out, f"expected={expected!r} actual={out!r}"


def test_stdout_no_extra_whitespace_or_lines():
    out = _load_module_capture_output("06_dictAccessAndTypes.py")
    expected_lines = ["Ada", "36", "<class 'int'>"]
    actual_lines = out.splitlines()
    assert expected_lines == actual_lines, f"expected={expected_lines!r} actual={actual_lines!r}"


def test_person_dict_exists_and_types():
    path = os.path.join(os.path.dirname(__file__), "06_dictAccessAndTypes.py")
    spec = importlib.util.spec_from_file_location("student_mod_06b", path)
    module = importlib.util.module_from_spec(spec)

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old

    assert hasattr(module, "person"), f"expected={'person'} actual={dir(module)!r}"
    person = module.person
    assert isinstance(person, dict), f"expected={dict} actual={type(person)}"
    assert "name" in person, f"expected={'name'} actual={list(person.keys())!r}"
    assert "age" in person, f"expected={'age'} actual={list(person.keys())!r}"
    assert isinstance(person["age"], int), f"expected={int} actual={type(person['age'])}"