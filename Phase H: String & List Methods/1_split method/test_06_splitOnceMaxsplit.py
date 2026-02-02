import importlib
import io
import contextlib


def test_split_once_maxsplit_output():
    mod = importlib.import_module("06_splitOnceMaxsplit")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    out = buf.getvalue().strip()
    expected = "header | a:b:c"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_split_once_maxsplit_no_extra_lines():
    mod = importlib.import_module("06_splitOnceMaxsplit")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    lines = [ln for ln in buf.getvalue().splitlines() if ln.strip() != ""]
    expected_count = 1
    actual_count = len(lines)
    assert actual_count == expected_count, f"expected={expected_count!r} actual={actual_count!r}"


def test_split_once_maxsplit_preserves_additional_colons():
    mod = importlib.import_module("06_splitOnceMaxsplit")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    out = buf.getvalue().strip()
    expected_suffix = "a:b:c"
    actual_suffix = out.split("|", 1)[1].strip() if "|" in out else ""
    assert actual_suffix == expected_suffix, f"expected={expected_suffix!r} actual={actual_suffix!r}"