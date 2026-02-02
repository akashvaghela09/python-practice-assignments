import importlib.util
import io
import os
import sys


def _load_module_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_program_output_exact():
    path = os.path.join(os.path.dirname(__file__), "09_deMorganPractice.py")
    buf = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buf
        _load_module_from_path("de_morgan_practice_09", path)
    finally:
        sys.stdout = old_stdout

    actual = buf.getvalue()
    expected = "original: False\nequivalent: False\nmatch: True\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_original_and_equivalent_match_and_are_booleans():
    path = os.path.join(os.path.dirname(__file__), "09_deMorganPractice.py")
    module = _load_module_from_path("de_morgan_practice_09_values", path)

    assert hasattr(module, "original")
    assert hasattr(module, "equivalent")
    assert hasattr(module, "match")

    assert isinstance(module.original, bool), f"expected={bool!r} actual={type(module.original)!r}"
    assert isinstance(module.equivalent, bool), f"expected={bool!r} actual={type(module.equivalent)!r}"
    assert isinstance(module.match, bool), f"expected={bool!r} actual={type(module.match)!r}"

    actual = (module.original == module.equivalent)
    expected = True
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_equivalent_has_no_parenthesized_not():
    path = os.path.join(os.path.dirname(__file__), "09_deMorganPractice.py")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    forbidden_patterns = [
        "equivalent = not (",
        "equivalent=not (",
        "equivalent = not(",
        "equivalent=not(",
    ]
    found = any(p in src for p in forbidden_patterns)
    assert found is False, f"expected={False!r} actual={found!r}"