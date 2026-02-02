import importlib
import io
import contextlib
import ast


def _load_module():
    return importlib.import_module("02_singletonTupleAndLen")


def test_singleton_tuple_exists_and_is_tuple():
    mod = _load_module()
    assert hasattr(mod, "singleton")
    assert isinstance(mod.singleton, tuple)


def test_singleton_tuple_has_one_element_and_correct_value():
    mod = _load_module()
    assert len(mod.singleton) == 1
    assert mod.singleton[0] == "only"


def test_printed_output_is_length_one():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = _load_module()
    out = buf.getvalue().strip()
    assert out == "1", f"expected='1' actual={out!r}"


def test_source_uses_singleton_tuple_syntax():
    with open("02_singletonTupleAndLen.py", "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    assigns = [
        n for n in tree.body
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "singleton" for t in n.targets)
    ]
    assert assigns
    value = assigns[0].value
    assert isinstance(value, ast.Tuple)
    assert len(value.elts) == 1
    assert isinstance(value.elts[0], ast.Constant)
    assert value.elts[0].value == "only"