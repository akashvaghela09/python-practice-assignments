import importlib.util
import pathlib
import re
import subprocess
import sys


FILE_NAME = "07_xorLikeLogic.py"


def _run_script():
    p = subprocess.run(
        [sys.executable, FILE_NAME],
        capture_output=True,
        text=True,
        cwd=pathlib.Path(__file__).resolve().parent,
    )
    return p.returncode, p.stdout, p.stderr


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location("xor_like_logic_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_runs_without_error_and_matches_output_exactly():
    code, out, err = _run_script()
    assert code == 0, f"expected=0 actual={code}\nexpected='' actual_stderr={err!r}"
    assert out == "exactly_one_discount: True\n", f"expected={'exactly_one_discount: True\\n'!r} actual={out!r}"


def test_expression_placeholder_removed_from_source():
    src = (pathlib.Path(__file__).resolve().parent / FILE_NAME).read_text(encoding="utf-8")
    assert "???" not in src, f"expected={'no placeholder'} actual={'placeholder present'}"


def test_implementation_does_not_use_bitwise_xor_operator():
    src = (pathlib.Path(__file__).resolve().parent / FILE_NAME).read_text(encoding="utf-8")
    src_wo_strings = re.sub(r'(\".*?\"|\'.*?\')', "", src, flags=re.DOTALL)
    assert "^" not in src_wo_strings, f"expected={'no ^'} actual={'^ present'}"


def test_variable_value_is_boolean_true():
    mod = _load_module()
    val = getattr(mod, "exactly_one_discount")
    assert isinstance(val, bool), f"expected={bool} actual={type(val)}"
    assert val is True, f"expected={True} actual={val}"


def test_xor_logic_truth_table_via_expression_text():
    src = (pathlib.Path(__file__).resolve().parent / FILE_NAME).read_text(encoding="utf-8")
    m = re.search(r"^\s*exactly_one_discount\s*=\s*(.+?)\s*$", src, flags=re.MULTILINE)
    assert m is not None, f"expected={'assignment found'} actual={'not found'}"
    expr = m.group(1).strip()
    assert expr and "???" not in expr, f"expected={'non-placeholder expression'} actual={expr!r}"

    def eval_expr(has_coupon, is_member):
        return eval(expr, {"__builtins__": {}}, {"has_coupon": has_coupon, "is_member": is_member})

    expected = {
        (False, False): False,
        (True, False): True,
        (False, True): True,
        (True, True): False,
    }
    for (hc, im), exp in expected.items():
        actual = eval_expr(hc, im)
        assert actual == exp, f"expected={exp} actual={actual}"