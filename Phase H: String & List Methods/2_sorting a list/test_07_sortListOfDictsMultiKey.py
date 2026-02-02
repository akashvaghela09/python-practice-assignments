import importlib
import ast
import os
import sys
import pytest


def _load_module(monkeypatch):
    monkeypatch.setattr(sys, "path", [""] + list(sys.path))
    monkeypatch.setattr(sys, "modules", dict(sys.modules))
    mod = importlib.import_module("07_sortListOfDictsMultiKey")
    return importlib.reload(mod)


def _expected_sorted(people):
    return sorted(people, key=lambda d: (d["last"], d["age"]))


def test_people_sorted_in_place_and_correct_order(monkeypatch, capsys):
    mod = _load_module(monkeypatch)
    captured = capsys.readouterr()

    assert hasattr(mod, "people")
    people = mod.people

    assert isinstance(people, list)
    assert all(isinstance(x, dict) for x in people)

    expected = _expected_sorted(people)
    assert people == expected, f"expected={expected!r} actual={people!r}"

    expected2 = _expected_sorted(people)
    assert people == expected2, f"expected={expected2!r} actual={people!r}"

    assert captured.out.strip() != ""


def test_stable_multikey_sort_property(monkeypatch):
    mod = _load_module(monkeypatch)
    people = mod.people

    for i in range(len(people) - 1):
        a = (people[i]["last"], people[i]["age"])
        b = (people[i + 1]["last"], people[i + 1]["age"])
        assert a <= b, f"expected={a!r} actual={b!r}"


def test_file_contains_inplace_sort_not_reassignment():
    fname = "07_sortListOfDictsMultiKey.py"
    assert os.path.exists(fname)

    with open(fname, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src, filename=fname)

    has_people_assignment = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "people" for t in node.targets):
            if has_people_assignment:
                pytest.fail("expected=<single assignment to people> actual=<multiple assignments to people>")
            has_people_assignment = True

    assert has_people_assignment

    reassigned_after_init = False
    seen_first_people_assignment = False
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "people" for t in node.targets):
            if seen_first_people_assignment:
                reassigned_after_init = True
            else:
                seen_first_people_assignment = True

    assert not reassigned_after_init, "expected=<no reassignment> actual=<reassignment detected>"

    has_inplace_sort = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "people" and node.func.attr == "sort":
                has_inplace_sort = True
                break

    assert has_inplace_sort, "expected=<people.sort(...) used> actual=<not found>"


def test_inplace_sort_uses_multikey(monkeypatch):
    mod = _load_module(monkeypatch)
    people = mod.people

    lasts = [p["last"] for p in people]
    assert lasts == sorted(lasts), f"expected={sorted(lasts)!r} actual={lasts!r}"

    from collections import defaultdict

    by_last = defaultdict(list)
    for p in people:
        by_last[p["last"]].append(p["age"])

    for last, ages in by_last.items():
        assert ages == sorted(ages), f"expected={sorted(ages)!r} actual={ages!r}"