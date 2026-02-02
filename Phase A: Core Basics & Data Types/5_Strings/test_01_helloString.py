import subprocess
import sys
import os
import importlib.util
import re
import pytest

FILE_NAME = "01_helloString.py"
EXPECTED = "Hello, world!\n"


def run_script():
    script_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    return subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        check=False,
    )


def test_program_exits_successfully():
    res = run_script()
    assert res.returncode == 0, f"expected=0 actual={res.returncode}"


def test_prints_expected_output_exactly():
    res = run_script()
    assert res.stdout == EXPECTED, f"expected={EXPECTED!r} actual={res.stdout!r}"


def test_no_extra_stderr_output():
    res = run_script()
    assert res.stderr == "", f"expected={''!r} actual={res.stderr!r}"


def test_message_variable_is_non_empty_and_matches_expected():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    spec = importlib.util.spec_from_file_location("hello_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert hasattr(mod, "message"), "expected=True actual=False"
    assert isinstance(mod.message, str), f"expected={str!r} actual={type(mod.message)!r}"
    assert mod.message == "Hello, world!", f"expected={'Hello, world!'!r} actual={mod.message!r}"
    assert mod.message != "", f"expected={'non-empty'!r} actual={mod.message!r}"


def test_source_contains_print_of_message():
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    has_print_message = re.search(r"^\s*print\s*\(\s*message\s*\)\s*$", src, re.MULTILINE) is not None
    assert has_print_message, f"expected={True!r} actual={has_print_message!r}"