import importlib.util
import pathlib
import sys
import types
import pytest

MODULE_FILENAME = "14_noMutationFunction.py"


def load_module(tmp_path, content):
    p = tmp_path / MODULE_FILENAME
    p.write_text(content, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("student_module_14", str(p))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["student_module_14"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def assignment_content():
    return """# Goal: Write a function that accepts a tuple and returns a modified NEW tuple without mutating input.
# Expected outcome:
# - Prints: "in: (10, 20, 30)"
# - Prints: "out: (10, 99, 30)"
# - Prints: "same input object: True" (input variable still refers to original tuple)

def replace_at(t, index, value):
    \"\"\"Return a new tuple equal to t but with t[index] replaced by value.\"\"\"
    # TODO: implement using slicing and concatenation
    pass

inp = (10, 20, 30)
out = replace_at(inp, 1, 99)

print("in:", inp)
print("out:", out)
print("same input object:", inp is (10, 20, 30))
"""


def test_import_prints_expected_lines(tmp_path, capsys, assignment_content):
    load_module(tmp_path, assignment_content)
    captured = capsys.readouterr().out.strip().splitlines()
    expected = [
        "in: (10, 20, 30)",
        "out: (10, 99, 30)",
        "same input object: True",
    ]
    assert captured == expected, f"expected={expected!r} actual={captured!r}"


def test_replace_at_returns_new_tuple_and_does_not_mutate(tmp_path, assignment_content):
    mod = load_module(tmp_path, assignment_content)

    inp = (10, 20, 30)
    original_id = id(inp)
    out = mod.replace_at(inp, 1, 99)

    assert inp == (10, 20, 30), f"expected={(10, 20, 30)!r} actual={inp!r}"
    assert id(inp) == original_id, f"expected={original_id!r} actual={id(inp)!r}"

    assert isinstance(out, tuple), f"expected={tuple!r} actual={type(out)!r}"
    assert out == (10, 99, 30), f"expected={(10, 99, 30)!r} actual={out!r}"
    assert out is not inp, f"expected={'different objects'!r} actual={'same object' if out is inp else 'different objects'!r}"


@pytest.mark.parametrize(
    "t,index,value,expected",
    [
        ((1, 2, 3, 4), 0, 9, (9, 2, 3, 4)),
        ((1, 2, 3, 4), 3, 9, (1, 2, 3, 9)),
        ((1, 2, 3, 4), -1, 9, (1, 2, 3, 9)),
        (("a", "b", "c"), 1, "x", ("a", "x", "c")),
        ((True, False), 0, False, (False, False)),
    ],
)
def test_replace_at_various_indices(tmp_path, assignment_content, t, index, value, expected):
    mod = load_module(tmp_path, assignment_content)
    original = tuple(t)
    out = mod.replace_at(t, index, value)

    assert t == original, f"expected={original!r} actual={t!r}"
    assert out == expected, f"expected={expected!r} actual={out!r}"
    assert out is not t, f"expected={'different objects'!r} actual={'same object' if out is t else 'different objects'!r}"


@pytest.mark.parametrize("index", [5, -6])
def test_replace_at_out_of_range_raises(tmp_path, assignment_content, index):
    mod = load_module(tmp_path, assignment_content)
    t = (1, 2, 3)
    with pytest.raises(IndexError):
        mod.replace_at(t, index, 9)


def test_replace_at_rejects_non_tuple_input(tmp_path, assignment_content):
    mod = load_module(tmp_path, assignment_content)
    with pytest.raises(TypeError):
        mod.replace_at([1, 2, 3], 1, 9)