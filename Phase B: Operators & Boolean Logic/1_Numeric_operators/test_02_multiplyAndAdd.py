import importlib.util
import pathlib
import re


def _run_module_capture_stdout(module_name, file_path, capsys):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return module, out


def test_prints_exact_output(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "02_multiplyAndAdd.py"
    _, out = _run_module_capture_stdout("m02_multiplyAndAdd_out", file_path, capsys)
    expected = "Bill: 68\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_bill_value_is_correct(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "02_multiplyAndAdd.py"
    mod, _ = _run_module_capture_stdout("m02_multiplyAndAdd_val", file_path, capsys)
    expected = 68
    actual = getattr(mod, "bill", object())
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_bill_is_int(capsys):
    file_path = pathlib.Path(__file__).resolve().parent / "02_multiplyAndAdd.py"
    mod, _ = _run_module_capture_stdout("m02_multiplyAndAdd_type", file_path, capsys)
    expected = int
    actual = type(getattr(mod, "bill", None))
    assert actual is expected, f"expected={expected!r} actual={actual!r}"


def test_expression_uses_multiply_and_add_in_source():
    file_path = pathlib.Path(__file__).resolve().parent / "02_multiplyAndAdd.py"
    src = file_path.read_text(encoding="utf-8")

    src_no_comments = re.sub(r"(?m)^\s*#.*$", "", src)
    match = re.search(r"(?m)^\s*bill\s*=\s*(.+?)\s*$", src_no_comments)
    assert match is not None, f"expected={True!r} actual={False!r}"

    rhs = match.group(1).strip()
    has_mul = "*" in rhs
    has_add = "+" in rhs
    expected = (True, True)
    actual = (has_mul, has_add)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"