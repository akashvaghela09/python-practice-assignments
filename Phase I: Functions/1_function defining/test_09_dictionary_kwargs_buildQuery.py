import importlib
import ast
import io
import contextlib
import re
import pytest

MODULE_NAME = "09_dictionary_kwargs_buildQuery"


def _import_module():
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def _parse_kv_pairs(s):
    parts = s.split("&") if s else []
    pairs = []
    for p in parts:
        if "=" not in p:
            raise ValueError("bad_pair")
        k, v = p.split("=", 1)
        pairs.append((k, v))
    return pairs


def test_build_query_exists_and_callable():
    mod, _ = _import_module()
    assert hasattr(mod, "build_query")
    assert callable(mod.build_query)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"b": 2, "a": 1},
        {"page": 2, "q": "python"},
        {"z": 0, "a": 10, "m": 5},
        {"x": None, "y": True, "z": 3.5},
    ],
)
def test_build_query_format_and_sorting(kwargs):
    mod, _ = _import_module()
    out = mod.build_query(**kwargs)
    assert isinstance(out, str)

    pairs = _parse_kv_pairs(out)
    keys = [k for k, _ in pairs]

    expected_keys = sorted(kwargs.keys())
    assert keys == expected_keys

    out_map = {k: v for k, v in pairs}
    expected_map = {k: str(v) for k, v in kwargs.items()}
    assert out_map == expected_map


def test_build_query_empty_kwargs_returns_empty_string():
    mod, _ = _import_module()
    out = mod.build_query()
    assert out == ""


def test_module_prints_two_lines_exactly():
    mod, captured = _import_module()
    lines = captured.splitlines()
    assert len(lines) == 2

    assert lines[0] == "page=2&q=python"
    assert lines[1] == "a=10&m=5&z=0"


def test_source_uses_kwargs_signature_and_sorted_keys():
    import inspect

    mod, _ = _import_module()
    sig = inspect.signature(mod.build_query)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].kind == inspect.Parameter.VAR_KEYWORD

    src = inspect.getsource(mod.build_query)
    tree = ast.parse(src)

    has_sorted = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sorted":
            has_sorted = True
            break
    assert has_sorted


def test_no_trailing_ampersand_and_no_spaces():
    mod, _ = _import_module()
    out = mod.build_query(c=3, a=1, b=2)
    assert " " not in out
    assert not out.endswith("&")
    assert re.fullmatch(r"[A-Za-z_]\w*=[^&]*(&[A-Za-z_]\w*=[^&]*)*", out) is not None