import ast
import importlib.util
import io
import os
import sys
import contextlib

MODULE_FILE = "10_filterTruthyValues.py"
MODULE_NAME = "mod_10_filterTruthyValues"


def _load_module():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_script_capture_stdout():
    path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        namespace = {"__name__": "__main__"}
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, path, "exec"), namespace, namespace)
    return buf.getvalue()


def test_script_prints_expected_exact_output():
    out = _run_script_capture_stdout()
    lines = out.splitlines()
    assert len(lines) == 1, f"expected one line, actual lines: {lines}"
    expected = "[1, 'hi', [0], True, {'x': 1}]"
    assert lines[0] == expected, f"expected: {expected!r}, actual: {lines[0]!r}"


def test_keep_truthy_filters_falsy_preserves_order_and_identity():
    m = _load_module()

    inner_list = [0]
    inner_dict = {"x": 1}
    sentinel_obj = object()

    data = [
        0,
        1,
        "",
        "hi",
        [],
        inner_list,
        None,
        False,
        True,
        {},
        inner_dict,
        sentinel_obj,
    ]

    res = m.keep_truthy(data)

    expected = [1, "hi", inner_list, True, inner_dict, sentinel_obj]
    assert res == expected, f"expected: {expected!r}, actual: {res!r}"
    assert res[2] is inner_list, f"expected: {inner_list!r}, actual: {res[2]!r}"
    assert res[4] is inner_dict, f"expected: {inner_dict!r}, actual: {res[4]!r}"
    assert res[5] is sentinel_obj, f"expected: {sentinel_obj!r}, actual: {res[5]!r}"


def test_keep_truthy_does_not_mutate_input():
    m = _load_module()
    data = [0, 1, "", "hi", [], [0], None, False, True, {}, {"x": 1}]
    before = list(data)
    _ = m.keep_truthy(data)
    assert data == before, f"expected: {before!r}, actual: {data!r}"


def test_keep_truthy_empty_input_returns_empty():
    m = _load_module()
    res = m.keep_truthy([])
    assert res == [], f"expected: {[]!r}, actual: {res!r}"


def test_keep_truthy_handles_other_falsy_values():
    m = _load_module()
    data = [0.0, set(), (), b"", bytearray(b""), -1, "0", [1], {"a": 0}]
    res = m.keep_truthy(data)
    expected = [-1, "0", [1], {"a": 0}]
    assert res == expected, f"expected: {expected!r}, actual: {res!r}"


def test_keep_truthy_function_exists_and_callable():
    m = _load_module()
    assert hasattr(m, "keep_truthy"), f"expected: {'keep_truthy'!r}, actual: {dir(m)!r}"
    assert callable(m.keep_truthy), f"expected: {'callable'!r}, actual: {type(m.keep_truthy)!r}"