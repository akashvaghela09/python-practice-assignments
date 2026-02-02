import ast
import importlib
import io
import contextlib


def _load_module():
    return importlib.import_module("07_invertMappingUnique")


def _parse_last_dict_from_stdout(out: str):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    assert lines, f"expected=non_empty_output actual={out!r}"
    last = lines[-1]
    try:
        node = ast.parse(last, mode="eval").body
    except SyntaxError as e:
        assert False, f"expected=dict_literal actual={last!r}"
    if not isinstance(node, ast.Dict):
        assert False, f"expected=dict_literal actual={last!r}"
    try:
        val = ast.literal_eval(ast.Expression(node))
    except Exception:
        val = ast.literal_eval(last)
    return val


def test_inverted_variable_is_correct_dict():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module()
    assert hasattr(mod, "original"), f"expected=has_original actual={dir(mod)!r}"
    assert hasattr(mod, "inverted"), f"expected=has_inverted actual={dir(mod)!r}"
    expected = {v: k for k, v in mod.original.items()}
    assert isinstance(mod.inverted, dict), f"expected=dict actual={type(mod.inverted).__name__}"
    assert mod.inverted == expected, f"expected={expected!r} actual={mod.inverted!r}"


def test_printed_output_matches_inverted_variable():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module()
    out = buf.getvalue()
    printed_dict = _parse_last_dict_from_stdout(out)
    assert printed_dict == mod.inverted, f"expected={mod.inverted!r} actual={printed_dict!r}"


def test_inverted_is_true_inverse_of_original():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module()
    inv = mod.inverted
    orig = mod.original
    ok = all(inv.get(v, object()) == k for k, v in orig.items())
    assert ok, f"expected=all_pairs_inverted actual={[(k,v,inv.get(v,None)) for k,v in orig.items()]!r}"