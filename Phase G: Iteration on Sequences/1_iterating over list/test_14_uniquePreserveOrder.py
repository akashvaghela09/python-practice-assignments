import ast
import importlib.util
import io
import os
import sys
import contextlib
import pytest


FILE_NAME = "14_uniquePreserveOrder.py"


def _load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _load_module_from_path(path, f"_student_mod_{os.path.basename(path).replace('.','_')}")
    return buf.getvalue()


def _parse_last_list_from_stdout(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        val = ast.literal_eval(last)
    except Exception:
        return None
    return val


def test_runs_without_error(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")
    try:
        _run_script_capture_stdout(str(dst))
    except Exception as e:
        pytest.fail(f"expected no exception, actual {type(e).__name__}: {e}")


def test_prints_list(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")
    out = _run_script_capture_stdout(str(dst))
    val = _parse_last_list_from_stdout(out)
    assert isinstance(val, list), f"expected list, actual {type(val).__name__}"


def test_output_matches_preserve_first_occurrence(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    out = _run_script_capture_stdout(str(dst))
    printed = _parse_last_list_from_stdout(out)

    module = _load_module_from_path(str(dst), "_student_mod_for_expected")
    assert hasattr(module, "items"), "expected items present, actual missing"

    expected = []
    seen = set()
    for x in module.items:
        if x not in seen:
            expected.append(x)
            seen.add(x)

    assert printed == expected, f"expected {expected!r}, actual {printed!r}"


def test_module_variables_types_and_consistency(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    module = _load_module_from_path(str(dst), "_student_mod_vars")
    assert hasattr(module, "unique"), "expected unique present, actual missing"
    assert hasattr(module, "seen"), "expected seen present, actual missing"

    unique = module.unique
    seen = module.seen
    assert isinstance(unique, list), f"expected list, actual {type(unique).__name__}"
    assert isinstance(seen, set), f"expected set, actual {type(seen).__name__}"

    assert len(unique) == len(seen), f"expected equal lengths, actual {len(unique)} vs {len(seen)}"
    assert set(unique) == seen, f"expected same elements, actual {set(unique)!r} vs {seen!r}"


def test_unique_preserves_order_of_first_occurrence(tmp_path):
    src = os.path.join(os.path.dirname(__file__), FILE_NAME)
    dst = tmp_path / FILE_NAME
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    module = _load_module_from_path(str(dst), "_student_mod_order")
    items = getattr(module, "items", None)
    unique = getattr(module, "unique", None)

    assert isinstance(items, list), f"expected list, actual {type(items).__name__}"
    assert isinstance(unique, list), f"expected list, actual {type(unique).__name__}"

    first_index = {}
    for i, x in enumerate(items):
        if x not in first_index:
            first_index[x] = i

    expected_order = sorted(first_index.items(), key=lambda kv: kv[1])
    expected_unique = [k for k, _ in expected_order]

    assert unique == expected_unique, f"expected {expected_unique!r}, actual {unique!r}"