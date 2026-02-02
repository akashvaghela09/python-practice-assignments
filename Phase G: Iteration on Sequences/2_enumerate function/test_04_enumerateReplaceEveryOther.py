import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest

MODULE_FILE = "04_enumerateReplaceEveryOther.py"


def _load_module():
    if not os.path.exists(MODULE_FILE):
        pytest.skip(f"Missing file: {MODULE_FILE}")
    name = "student_mod_04_enumerateReplaceEveryOther"
    spec = importlib.util.spec_from_file_location(name, MODULE_FILE)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            return mod, buf.getvalue(), e
    return mod, buf.getvalue(), None


def _parse_printed_list(stdout):
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        return ast.literal_eval(last)
    except Exception:
        return None


def test_module_executes_without_error():
    mod, out, err = _load_module()
    assert err is None, f"expected={None!r} actual={repr(err)}"


def test_words_variable_exists_and_is_list():
    mod, out, err = _load_module()
    if err is not None:
        pytest.fail(f"expected={None!r} actual={repr(err)}")
    assert hasattr(mod, "words"), f"expected={'words attribute'!r} actual={dir(mod)!r}"
    assert isinstance(mod.words, list), f"expected={list!r} actual={type(mod.words)!r}"


def test_replaces_every_other_word_with_underscore():
    mod, out, err = _load_module()
    if err is not None:
        pytest.fail(f"expected={None!r} actual={repr(err)}")
    expected = ["keep", "_", "keep", "_", "keep"]
    assert mod.words == expected, f"expected={expected!r} actual={mod.words!r}"


def test_printed_output_matches_final_words_list():
    mod, out, err = _load_module()
    if err is not None:
        pytest.fail(f"expected={None!r} actual={repr(err)}")
    printed = _parse_printed_list(out)
    assert printed == mod.words, f"expected={mod.words!r} actual={printed!r}"


def test_underscore_only_at_odd_indices():
    mod, out, err = _load_module()
    if err is not None:
        pytest.fail(f"expected={None!r} actual={repr(err)}")
    expected_positions = [i for i, v in enumerate(mod.words) if v == "_"]
    assert expected_positions == [1, 3], f"expected={[1, 3]!r} actual={expected_positions!r}"


def test_source_uses_enumerate():
    if not os.path.exists(MODULE_FILE):
        pytest.skip(f"Missing file: {MODULE_FILE}")
    with open(MODULE_FILE, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    uses_enumerate = any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "enumerate"
        for n in ast.walk(tree)
    )
    assert uses_enumerate is True, f"expected={True!r} actual={uses_enumerate!r}"