import ast
import importlib
import pathlib
import sys


MODULE_NAME = "15_mutableObjectIdentityTracker"


def _run_main_capture_output(monkeypatch):
    mod = importlib.import_module(MODULE_NAME)
    out = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        out.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr(mod, "print", fake_print)
    mod.main()
    return "".join(out)


def _parse_kv_lines(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip() != ""]
    kv = {}
    for ln in lines:
        if ":" not in ln:
            continue
        k, v = ln.split(":", 1)
        kv[k.strip()] = v.strip()
    return lines, kv


def test_main_prints_exact_lines(monkeypatch):
    output = _run_main_capture_output(monkeypatch)
    lines = output.splitlines()
    assert len(lines) == 4, f"expected={4!r} actual={len(lines)!r}"
    assert lines[0] == "same_after_mutation: True", f"expected={'same_after_mutation: True'!r} actual={lines[0]!r}"
    assert lines[1] == "same_after_shallow_copy: False", f"expected={'same_after_shallow_copy: False'!r} actual={lines[1]!r}"
    assert lines[2] == "alias_reflects_change: True", f"expected={'alias_reflects_change: True'!r} actual={lines[2]!r}"
    assert lines[3].startswith("final: "), f"expected={True!r} actual={lines[3].startswith('final: ')!r}"


def test_final_dict_structure_and_contents(monkeypatch):
    output = _run_main_capture_output(monkeypatch)
    lines, kv = _parse_kv_lines(output)

    assert "final" in kv, f"expected={True!r} actual={('final' in kv)!r}"
    final_str = kv["final"]
    final_obj = ast.literal_eval(final_str)

    assert isinstance(final_obj, dict), f"expected={dict!r} actual={type(final_obj)!r}"
    assert set(final_obj.keys()) == {"a", "b", "c"}, f"expected={{'a','b','c'}!r} actual={set(final_obj.keys())!r}"

    a = final_obj["a"]
    b = final_obj["b"]
    c = final_obj["c"]

    assert a == b, f"expected={a!r} actual={b!r}"
    assert a != c, f"expected={False!r} actual={(a == c)!r}"

    assert isinstance(a, list), f"expected={list!r} actual={type(a)!r}"
    assert isinstance(b, list), f"expected={list!r} actual={type(b)!r}"
    assert isinstance(c, list), f"expected={list!r} actual={type(c)!r}"

    assert a == [1, 2, 3, 4], f"expected={[1,2,3,4]!r} actual={a!r}"
    assert b == [1, 2, 3, 4], f"expected={[1,2,3,4]!r} actual={b!r}"
    assert c == [1, 2, 3], f"expected={[1,2,3]!r} actual={c!r}"


def test_alias_and_shallow_copy_semantics_via_output(monkeypatch):
    output = _run_main_capture_output(monkeypatch)
    _, kv = _parse_kv_lines(output)

    assert kv.get("same_after_mutation") == "True", f"expected={'True'!r} actual={kv.get('same_after_mutation')!r}"
    assert kv.get("same_after_shallow_copy") == "False", f"expected={'False'!r} actual={kv.get('same_after_shallow_copy')!r}"
    assert kv.get("alias_reflects_change") == "True", f"expected={'True'!r} actual={kv.get('alias_reflects_change')!r}"


def test_source_file_exists_and_importable():
    path = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    assert path.exists(), f"expected={True!r} actual={path.exists()!r}"
    mod = importlib.import_module(MODULE_NAME)
    assert hasattr(mod, "main"), f"expected={True!r} actual={hasattr(mod, 'main')!r}"