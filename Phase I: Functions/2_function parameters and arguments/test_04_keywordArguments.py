import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILE = "04_keywordArguments.py"


def load_module(tmp_path, content):
    file_path = tmp_path / MODULE_FILE
    file_path.write_text(content, encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod", str(file_path))
    module = importlib.util.module_from_spec(spec)

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(module)
    finally:
        sys.stdout = old

    return module, buf.getvalue()


def test_module_prints_expected_output(tmp_path):
    content = open(MODULE_FILE, "r", encoding="utf-8").read()
    _, out = load_module(tmp_path, content)
    expected = "2, 5, 9\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_pack_returns_correct_string(tmp_path):
    content = open(MODULE_FILE, "r", encoding="utf-8").read()
    module, _ = load_module(tmp_path, content)
    expected = "2, 5, 9"
    actual = module.pack(c=9, a=2, b=5)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_pack_accepts_keyword_reordering(tmp_path):
    content = open(MODULE_FILE, "r", encoding="utf-8").read()
    module, _ = load_module(tmp_path, content)
    expected = "1, 2, 3"
    actual = module.pack(b=2, c=3, a=1)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_pack_preserves_values_as_strings(tmp_path):
    content = open(MODULE_FILE, "r", encoding="utf-8").read()
    module, _ = load_module(tmp_path, content)
    expected = "x, None, 0"
    actual = module.pack("x", None, 0)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"