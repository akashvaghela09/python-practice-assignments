import importlib
import contextlib
import io
import ast
import pathlib
import sys

MODULE_NAME = "08_loginStatus"


def _load_module():
    if MODULE_NAME in sys.modules:
        return importlib.reload(sys.modules[MODULE_NAME])
    return importlib.import_module(MODULE_NAME)


def _run_with_vars(username, password, locked):
    mod = importlib.import_module(MODULE_NAME)
    mod.username = username
    mod.password = password
    mod.locked = locked
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    out = buf.getvalue().splitlines()
    return out


def test_expected_given_example_missing_username():
    out = _run_with_vars("", "abc", False)
    assert out == ["Missing username"]


def test_missing_password_when_username_present():
    out = _run_with_vars("admin", "", False)
    assert out == ["Missing password"]


def test_account_locked_overrides_correct_credentials():
    out = _run_with_vars("admin", "s3cr3t", True)
    assert out == ["Account locked"]


def test_access_granted_when_credentials_correct_and_not_locked():
    out = _run_with_vars("admin", "s3cr3t", False)
    assert out == ["Access granted"]


def test_access_denied_when_credentials_incorrect():
    out = _run_with_vars("admin", "wrong", False)
    assert out == ["Access denied"]


def test_prints_exactly_one_line():
    out = _run_with_vars("x", "y", False)
    assert len(out) == 1


def test_no_extra_whitespace_in_output_line():
    out = _run_with_vars("x", "y", False)
    assert out[0] == out[0].strip()


def test_has_if_elif_else_structure_in_source():
    path = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    if_nodes = [n for n in tree.body if isinstance(n, ast.If)]
    assert if_nodes, "expected_if_vs_actual_none"

    top = if_nodes[0]
    assert top.orelse, "expected_elif_or_else_vs_actual_missing"
    assert isinstance(top.orelse[0], ast.If) or isinstance(top.orelse[0], ast.Expr) or isinstance(
        top.orelse[0], ast.If
    )

    chain_len = 1
    cur = top
    while cur.orelse and isinstance(cur.orelse[0], ast.If):
        chain_len += 1
        cur = cur.orelse[0]
    assert chain_len >= 4, f"expected_chain_len>=4_vs_actual_{chain_len}"


def test_only_one_print_statement_present():
    path = pathlib.Path(__file__).with_name(f"{MODULE_NAME}.py")
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    prints = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
    ]
    assert len(prints) == 1, f"expected_print_calls_1_vs_actual_{len(prints)}"