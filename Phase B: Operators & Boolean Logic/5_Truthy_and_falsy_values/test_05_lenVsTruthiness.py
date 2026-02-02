import importlib.util
import io
import os
import contextlib
import pytest

ASSIGNMENT_FILE = "05_lenVsTruthiness.py"


def load_module_from_path(path, module_name="student_module"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prints_ready(tmp_path, capsys):
    target = tmp_path / ASSIGNMENT_FILE
    target.write_text(open(ASSIGNMENT_FILE, "r", encoding="utf-8").read(), encoding="utf-8")

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        load_module_from_path(str(target), module_name="m1")

    actual = buf.getvalue()
    expected = "READY\n"
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_uses_truthiness_not_len(tmp_path):
    target = tmp_path / ASSIGNMENT_FILE
    target.write_text(open(ASSIGNMENT_FILE, "r", encoding="utf-8").read(), encoding="utf-8")

    source = target.read_text(encoding="utf-8")
    lowered = source.replace(" ", "").replace("\t", "").lower()
    assert "len(" not in lowered, f"expected={'no len(...) usage'!r} actual={'len(...) found'!r}"


def test_if_condition_references_queue(tmp_path):
    target = tmp_path / ASSIGNMENT_FILE
    target.write_text(open(ASSIGNMENT_FILE, "r", encoding="utf-8").read(), encoding="utf-8")

    source = target.read_text(encoding="utf-8")
    assert "if queue" in source, f"expected={'if condition uses queue'!r} actual={'if condition does not use queue'!r}"