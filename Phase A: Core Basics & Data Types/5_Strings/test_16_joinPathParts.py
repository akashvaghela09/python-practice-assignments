import importlib
import io
import contextlib


def test_joined_path_output():
    mod_name = "16_joinPathParts"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    actual = buf.getvalue().strip()
    expected = "api/v1/users"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"