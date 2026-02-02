import ast
import importlib.util
import io
import os
import sys
import types
import pytest

MODULE_FILENAME = "07_reverseAndJoin.py"


def _load_module_from_file(tmp_path):
    src = (tmp_path / MODULE_FILENAME).read_text(encoding="utf-8")
    mod_name = "student_mod_07_reverseAndJoin"
    spec = importlib.util.spec_from_loader(mod_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(tmp_path / MODULE_FILENAME)
    code = compile(src, str(tmp_path / MODULE_FILENAME), "exec")
    exec(code, module.__dict__)
    return module, src


def _run_file_capture_stdout(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        src = (tmp_path / MODULE_FILENAME).read_text(encoding="utf-8")
        glb = {"__name__": "__main__", "__file__": str(tmp_path / MODULE_FILENAME)}
        exec(compile(src, str(tmp_path / MODULE_FILENAME), "exec"), glb)
    finally:
        sys.stdout = old
    return buf.getvalue()


def _parse_output(stdout):
    reversed_val = None
    joined_val = None
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("reversed="):
            reversed_val = line.split("=", 1)[1]
        elif line.startswith("joined="):
            joined_val = line.split("=", 1)[1]
    return reversed_val, joined_val


def _assert_eq(expected, actual):
    assert expected == actual, f"expected={expected!r} actual={actual!r}"


@pytest.fixture
def tmp_assignment(tmp_path):
    content = (
        '# Goal: reverse a list and build a string from list items.\n'
        '# Expected outcome (print output):\n'
        '# reversed=["c", "b", "a"]\n'
        '# joined=c-b-a\n'
        '\n'
        'parts = ["a", "b", "c"]\n'
        '\n'
        '# TODO: create reversed_parts as a NEW list in reverse order (do not mutate parts)\n'
        'reversed_parts =\n'
        '\n'
        "# TODO: join reversed_parts with '-' into joined\n"
        'joined =\n'
        '\n'
        'print(f"reversed={reversed_parts}")\n'
        'print(f"joined={joined}")\n'
    )
    (tmp_path / MODULE_FILENAME).write_text(content, encoding="utf-8")
    return tmp_path


def test_file_exists_and_is_importable(tmp_assignment):
    path = tmp_assignment / MODULE_FILENAME
    assert path.exists(), f"expected={True!r} actual={path.exists()!r}"


def test_no_syntax_errors(tmp_assignment):
    src = (tmp_assignment / MODULE_FILENAME).read_text(encoding="utf-8")
    try:
        compile(src, str(tmp_assignment / MODULE_FILENAME), "exec")
    except SyntaxError as e:
        pytest.fail(f"expected={'no SyntaxError'!r} actual={str(e).splitlines()[0]!r}")


def test_printed_output_format_and_values(tmp_assignment, monkeypatch):
    stdout = _run_file_capture_stdout(tmp_assignment, monkeypatch)
    rev_s, joined_s = _parse_output(stdout)
    assert rev_s is not None, f"expected={'reversed line present'!r} actual={stdout!r}"
    assert joined_s is not None, f"expected={'joined line present'!r} actual={stdout!r}"

    expected_rev = str(["c", "b", "a"])
    expected_joined = "c-b-a"
    _assert_eq(expected_rev, rev_s)
    _assert_eq(expected_joined, joined_s)


def test_reversed_parts_is_new_list_and_parts_not_mutated(tmp_assignment, monkeypatch):
    module, _ = _load_module_from_file(tmp_assignment)
    assert isinstance(module.parts, list), f"expected={list!r} actual={type(module.parts)!r}"
    assert isinstance(module.reversed_parts, list), f"expected={list!r} actual={type(module.reversed_parts)!r}"
    assert module.parts is not module.reversed_parts, f"expected={'different objects'!r} actual={'same object'!r}"

    expected_parts = ["a", "b", "c"]
    expected_reversed = ["c", "b", "a"]
    _assert_eq(expected_parts, module.parts)
    _assert_eq(expected_reversed, module.reversed_parts)


def test_joined_matches_reversed_parts(tmp_assignment):
    module, _ = _load_module_from_file(tmp_assignment)
    expected_joined = "-".join(module.reversed_parts)
    _assert_eq(expected_joined, module.joined)


def test_does_not_use_inplace_reverse_on_parts(tmp_assignment):
    src = (tmp_assignment / MODULE_FILENAME).read_text(encoding="utf-8")
    tree = ast.parse(src)

    class Finder(ast.NodeVisitor):
        def __init__(self):
            self.found = False

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr == "reverse":
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "parts":
                    self.found = True
            self.generic_visit(node)

    f = Finder()
    f.visit(tree)
    assert f.found is False, f"expected={False!r} actual={True!r}"