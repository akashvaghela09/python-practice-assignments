import importlib.util
import os
import sys
import re


def _run_module_capture_stdout(tmp_path, monkeypatch):
    src = os.path.join(os.path.dirname(__file__), "11_replaceCharacters.py")
    dst = tmp_path / "11_replaceCharacters.py"
    dst.write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setattr(sys, "modules", dict(sys.modules), raising=False)
    sys.modules.pop("11_replaceCharacters", None)

    spec = importlib.util.spec_from_file_location("11_replaceCharacters", str(dst))
    mod = importlib.util.module_from_spec(spec)

    from io import StringIO
    buf = StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.stdout = old

    return mod, buf.getvalue()


def test_prints_fixed_date(tmp_path, monkeypatch):
    mod, out = _run_module_capture_stdout(tmp_path, monkeypatch)
    expected = "2026/02/02"
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_fixed_variable_matches_replacement(tmp_path, monkeypatch):
    mod, out = _run_module_capture_stdout(tmp_path, monkeypatch)
    assert hasattr(mod, "date")
    assert hasattr(mod, "fixed")
    expected = getattr(mod, "date").replace("-", "/")
    actual = getattr(mod, "fixed")
    assert actual == expected, f"expected={expected!r} actual={actual!r}"
    assert "-" not in actual, f"expected={'no-hyphen'} actual={actual!r}"
    assert re.fullmatch(r"\d{4}/\d{2}/\d{2}", actual) is not None, f"expected={'YYYY/MM/DD'} actual={actual!r}"


def test_output_matches_fixed_variable(tmp_path, monkeypatch):
    mod, out = _run_module_capture_stdout(tmp_path, monkeypatch)
    expected = str(getattr(mod, "fixed")).strip()
    actual = out.strip()
    assert actual == expected, f"expected={expected!r} actual={actual!r}"