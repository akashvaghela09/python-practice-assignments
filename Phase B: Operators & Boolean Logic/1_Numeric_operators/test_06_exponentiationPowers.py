import importlib
import io
import contextlib
import re


def test_exponentiation_output_exact():
    mod_name = "06_exponentiationPowers"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.import_module(mod_name)
    out = buf.getvalue()
    assert out == "2^10 = 1024\n", f"expected={repr('2^10 = 1024\\n')} actual={repr(out)}"


def test_no_placeholder_none_in_output():
    mod_name = "06_exponentiationPowers"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue()
    assert "None" not in out, f"expected={repr('output without None')} actual={repr(out)}"


def test_uses_power_operator():
    mod_name = "06_exponentiationPowers"
    m = importlib.import_module(mod_name)
    src = getattr(m, "__file__", None)
    assert src is not None
    with open(src, "r", encoding="utf-8") as f:
        code = f.read()
    has_powop = "**" in code
    assert has_powop, f"expected={repr('** present')} actual={repr('** absent')}"


def test_result_matches_pow_of_base_and_exp():
    mod_name = "06_exponentiationPowers"
    m = importlib.reload(importlib.import_module(mod_name))
    assert hasattr(m, "base") and hasattr(m, "exp") and hasattr(m, "result")
    expected = pow(m.base, m.exp)
    actual = m.result
    assert actual == expected, f"expected={repr(expected)} actual={repr(actual)}"


def test_output_format():
    mod_name = "06_exponentiationPowers"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(importlib.import_module(mod_name))
    out = buf.getvalue().strip("\n")
    assert re.fullmatch(r"\d+\^\d+ = \d+", out) is not None, f"expected={repr('digit^digit = digit')} actual={repr(out)}"