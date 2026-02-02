import importlib.util
import io
import os
import contextlib
import ast
import pytest

MODULE_FILENAME = "07_enumerateBuildDictIndexToValue.py"


def load_module_from_file(tmp_path):
    src = os.path.abspath(MODULE_FILENAME)
    if not os.path.exists(src):
        pytest.skip(f"Missing file: {MODULE_FILENAME}")
    dst = tmp_path / MODULE_FILENAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("student_mod", str(dst))
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            raise
    return mod, buf.getvalue()


def test_index_map_correct_and_printed(tmp_path):
    mod, out = load_module_from_file(tmp_path)
    assert hasattr(mod, "index_map")
    expected = {0: "red", 1: "green", 2: "blue"}
    actual = mod.index_map
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    printed = None
    for line in (out or "").splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("{") and s.endswith("}"):
            try:
                printed = ast.literal_eval(s)
            except Exception:
                pass
    assert printed == expected, f"expected={expected!r} actual={printed!r}"


def test_uses_enumerate(tmp_path):
    src = os.path.abspath(MODULE_FILENAME)
    if not os.path.exists(src):
        pytest.skip(f"Missing file: {MODULE_FILENAME}")
    code = open(src, "r", encoding="utf-8").read()
    tree = ast.parse(code)

    uses = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "enumerate":
            uses = True
            break
    assert uses is True, f"expected={True!r} actual={uses!r}"


def test_index_map_has_int_keys_and_str_values(tmp_path):
    mod, _ = load_module_from_file(tmp_path)
    actual = mod.index_map
    keys_ok = all(isinstance(k, int) for k in actual.keys())
    vals_ok = all(isinstance(v, str) for v in actual.values())
    assert keys_ok is True, f"expected={True!r} actual={keys_ok!r}"
    assert vals_ok is True, f"expected={True!r} actual={vals_ok!r}"