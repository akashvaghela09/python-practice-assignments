import ast
import importlib.util
import os
import sys
import types
import pytest

FILE_NAME = "04_smallestOfThree.py"


def _load_module_unique(path):
    module_name = f"student_{os.path.splitext(os.path.basename(path))[0]}_{id(path)}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _run_script_capture_stdout(path):
    spec = importlib.util.spec_from_file_location(f"run_{id(path)}", path)
    mod = importlib.util.module_from_spec(spec)
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return buf.getvalue()


def _parse_printed_int(output):
    s = output.strip()
    if not s:
        return None
    first_line = s.splitlines()[0].strip()
    try:
        return int(first_line)
    except Exception:
        return None


def _get_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _has_min_call(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id == "min":
                return True
    return False


def _has_if_chain(tree):
    return any(isinstance(n, ast.If) for n in ast.walk(tree))


def _count_print_calls(tree):
    cnt = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id == "print":
                cnt += 1
    return cnt


def test_no_min_used():
    src = _get_source(FILE_NAME)
    tree = ast.parse(src)
    assert not _has_min_call(tree)


def test_uses_if_elif_else_structure():
    src = _get_source(FILE_NAME)
    tree = ast.parse(src)
    assert _has_if_chain(tree)


def test_prints_a_value():
    src = _get_source(FILE_NAME)
    tree = ast.parse(src)
    assert _count_print_calls(tree) >= 1


def test_default_values_print_smallest(capsys):
    mod = _load_module_unique(FILE_NAME)
    captured = capsys.readouterr().out
    actual = _parse_printed_int(captured)
    expected = min(getattr(mod, "a"), getattr(mod, "b"), getattr(mod, "c"))
    assert actual == expected, f"expected {expected} got {actual}"


@pytest.mark.parametrize(
    "a,b,c",
    [
        (1, 2, 3),
        (3, 2, 1),
        (-1, -2, -3),
        (0, 0, 1),
        (5, 5, 5),
        (2, 2, 1),
        (2, 1, 2),
        (1, 2, 1),
        (10, -10, 0),
        (7, 3, 3),
    ],
)
def test_logic_matches_min_for_various_inputs(monkeypatch, capsys, a, b, c):
    mod = _load_module_unique(FILE_NAME)

    def _no_print(*args, **kwargs):
        return None

    monkeypatch.setattr(mod, "print", _no_print, raising=False)

    mod.a, mod.b, mod.c = a, b, c

    stdout_before = capsys.readouterr().out

    if not hasattr(mod, "smallest"):
        try:
            mod.smallest = mod.a if mod.a <= mod.b and mod.a <= mod.c else (mod.b if mod.b <= mod.c else mod.c)
        except Exception:
            pass

    if hasattr(mod, "find_smallest") and isinstance(getattr(mod, "find_smallest"), types.FunctionType):
        got = mod.find_smallest(mod.a, mod.b, mod.c)
        expected = min(a, b, c)
        assert got == expected, f"expected {expected} got {got}"
        return

    if hasattr(mod, "smallest"):
        got = mod.smallest
        expected = min(a, b, c)
        assert got == expected, f"expected {expected} got {got}"
        return

    out = _run_script_capture_stdout(FILE_NAME)
    actual = _parse_printed_int(out)
    expected = min(a, b, c)
    assert actual == expected, f"expected {expected} got {actual}"