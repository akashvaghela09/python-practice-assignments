import importlib
import contextlib
import io
import ast
import pathlib
import pytest


MODULE_NAME = "04_membershipAndCounting"


def _load_module():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod = importlib.import_module(MODULE_NAME)
    return mod, buf.getvalue()


def _parse_printed(output: str):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip() != ""]
    if len(lines) != 3:
        return None
    try:
        vals = [ast.literal_eval(ln) for ln in lines]
    except Exception:
        vals = lines
    return vals


def test_module_imports_without_error():
    _load_module()


def test_expected_values():
    mod, output = _load_module()
    expected_has_a = ("a" in mod.text)
    expected_has_z = ("z" in mod.text)
    expected_count_a = mod.text.count("a")

    assert hasattr(mod, "has_a")
    assert hasattr(mod, "has_z")
    assert hasattr(mod, "count_a")

    assert mod.has_a == expected_has_a, f"expected={expected_has_a!r} actual={mod.has_a!r}"
    assert mod.has_z == expected_has_z, f"expected={expected_has_z!r} actual={mod.has_z!r}"
    assert mod.count_a == expected_count_a, f"expected={expected_count_a!r} actual={mod.count_a!r}"

    printed = _parse_printed(output)
    assert printed is not None, f"expected={3!r} actual={len([ln for ln in output.splitlines() if ln.strip() != ''])!r}"
    assert printed[0] == expected_has_a, f"expected={expected_has_a!r} actual={printed[0]!r}"
    assert printed[1] == expected_has_z, f"expected={expected_has_z!r} actual={printed[1]!r}"
    assert printed[2] == expected_count_a, f"expected={expected_count_a!r} actual={printed[2]!r}"


def test_placeholders_removed():
    path = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    if not path.exists():
        pytest.skip(f"{MODULE_NAME}.py not found next to tests")
    content = path.read_text(encoding="utf-8")
    assert "__" not in content, f"expected={False!r} actual={('__' in content)!r}"