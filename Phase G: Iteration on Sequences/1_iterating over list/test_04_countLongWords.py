import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

FILE_NAME = "04_countLongWords.py"


def _load_module(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    return spec, mod


def test_no_placeholders_left_in_source():
    src_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    content = open(src_path, "r", encoding="utf-8").read()
    assert "____" not in content


def test_prints_correct_count(tmp_path):
    spec, mod = _load_module(tmp_path)

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)

    out = buf.getvalue().strip()
    assert re.fullmatch(r"-?\d+", out) is not None

    expected = sum(1 for w in ["tree", "apple", "sun", "water", "stone"] if len(w) >= 5)
    actual = int(out)
    assert expected == actual, f"expected={expected} actual={actual}"


def test_uses_words_list_as_given(tmp_path):
    spec, mod = _load_module(tmp_path)

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)

    assert hasattr(mod, "words")
    assert isinstance(mod.words, list)
    assert mod.words == ["tree", "apple", "sun", "water", "stone"]


def test_algorithm_matches_generalized_rule(tmp_path):
    spec, mod = _load_module(tmp_path)

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)

    actual = int(buf.getvalue().strip())
    expected = sum(1 for w in mod.words if isinstance(w, str) and len(w) >= 5)
    assert expected == actual, f"expected={expected} actual={actual}"