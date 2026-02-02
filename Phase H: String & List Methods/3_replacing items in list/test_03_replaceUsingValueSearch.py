import importlib
import ast
import contextlib
import io


def _import_with_output(module_name):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(module_name)
    return mod, buf.getvalue()


def _parse_printed_list(output):
    s = output.strip()
    return ast.literal_eval(s)


def test_prints_expected_list(capsys):
    mod, out = _import_with_output("03_replaceUsingValueSearch")
    actual = _parse_printed_list(out)
    expected = ["cat", "dog", "fish"]
    assert actual == expected, f"expected={expected} actual={actual}"


def test_pets_variable_updated():
    mod, _ = _import_with_output("03_replaceUsingValueSearch")
    expected = ["cat", "dog", "fish"]
    actual = getattr(mod, "pets", None)
    assert actual == expected, f"expected={expected} actual={actual}"


def test_uses_index_method_in_source():
    mod, _ = _import_with_output("03_replaceUsingValueSearch")
    src = open(mod.__file__, "r", encoding="utf-8").read()
    assert ".index(" in src, f"expected={True} actual={'.index(' in src}"