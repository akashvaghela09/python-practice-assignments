import importlib
import io
import contextlib
import ast
import os


def _load_module_with_output():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module("07_variableKeywordArgsReport")
    return mod, buf.getvalue()


def test_printed_output_matches_expected():
    _, out = _load_module_with_output()
    expected = "age=12; name=Ria\n"
    assert out == expected, f"expected={expected!r}, actual={out!r}"


def test_report_sorts_keys_and_formats_values():
    mod, _ = _load_module_with_output()
    actual = mod.report(z=1, a=2, m=3)
    expected = "a=2; m=3; z=1"
    assert actual == expected, f"expected={expected!r}, actual={actual!r}"


def test_report_with_string_and_int_values():
    mod, _ = _load_module_with_output()
    actual = mod.report(name="Ria", age=12)
    expected = "age=12; name=Ria"
    assert actual == expected, f"expected={expected!r}, actual={actual!r}"


def test_report_empty_kwargs_returns_empty_string():
    mod, _ = _load_module_with_output()
    actual = mod.report()
    expected = ""
    assert actual == expected, f"expected={expected!r}, actual={actual!r}"


def test_report_does_not_mutate_inputs():
    mod, _ = _load_module_with_output()
    d = {"b": 2, "a": 1}
    actual = mod.report(**d)
    expected = "a=1; b=2"
    assert actual == expected, f"expected={expected!r}, actual={actual!r}"
    assert d == {"b": 2, "a": 1}, f"expected={{'b': 2, 'a': 1}}, actual={d!r}"


def test_source_has_report_defined():
    path = os.path.join(os.path.dirname(__file__), "07_variableKeywordArgsReport.py")
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)

    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "report"]
    assert len(funcs) == 1, f"expected={1!r}, actual={len(funcs)!r}"

    fn = funcs[0]
    assert fn.args.vararg is None, f"expected={None!r}, actual={getattr(fn.args.vararg, 'arg', None)!r}"
    assert fn.args.kwarg is not None, f"expected={True!r}, actual={(fn.args.kwarg is not None)!r}"