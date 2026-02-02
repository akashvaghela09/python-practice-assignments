import importlib
import io
import contextlib
import ast
import pytest

MODULE_NAME = "13_hashingImmutableComposite"


def load_module_capture():
    mod = importlib.import_module(MODULE_NAME)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        importlib.reload(mod)
    return mod, buf.getvalue()


def test_stdout_format_and_values():
    mod, out = load_module_capture()
    lines = [ln.strip() for ln in out.strip().splitlines() if ln.strip()]
    assert len(lines) == 2, f"expected={2!r} actual={len(lines)!r}"
    assert lines[0].startswith("key hashable:"), f"expected={'key hashable:'!r} actual={lines[0]!r}"
    assert lines[1].startswith("lookup:"), f"expected={'lookup:'!r} actual={lines[1]!r}"
    assert lines[0] == "key hashable: True", f"expected={'key hashable: True'!r} actual={lines[0]!r}"
    assert lines[1] == "lookup: found", f"expected={'lookup: found'!r} actual={lines[1]!r}"


def test_key_is_immutable_tuple_and_uses_expected_components():
    mod, _ = load_module_capture()
    assert isinstance(mod.key, tuple), f"expected={tuple!r} actual={type(mod.key)!r}"
    assert len(mod.key) == 3, f"expected={3!r} actual={len(mod.key)!r}"
    assert mod.key[0] == mod.user["name"], f"expected={mod.user['name']!r} actual={mod.key[0]!r}"
    assert isinstance(mod.key[1], tuple), f"expected={tuple!r} actual={type(mod.key[1])!r}"
    assert tuple(mod.user["roles"]) == mod.key[1], f"expected={tuple(mod.user['roles'])!r} actual={mod.key[1]!r}"
    assert mod.key[2] == mod.user["region"], f"expected={mod.user['region']!r} actual={mod.key[2]!r}"


def test_hashability_flag_matches_actual_hashability():
    mod, _ = load_module_capture()
    try:
        hash(mod.key)
        actual = True
    except Exception:
        actual = False
    assert mod.key_hashable == actual, f"expected={actual!r} actual={mod.key_hashable!r}"


def test_cache_is_dict_and_lookup_works_with_same_structure_key():
    mod, _ = load_module_capture()
    assert isinstance(mod.cache, dict), f"expected={dict!r} actual={type(mod.cache)!r}"
    assert mod.key in mod.cache, f"expected={True!r} actual={(mod.key in mod.cache)!r}"
    expected = "found"
    actual = mod.cache.get(mod.key)
    assert actual == expected, f"expected={expected!r} actual={actual!r}"

    equivalent_key = (mod.user["name"], tuple(mod.user["roles"]), mod.user["region"])
    assert mod.cache.get(equivalent_key) == expected, f"expected={expected!r} actual={mod.cache.get(equivalent_key)!r}"


def test_source_does_not_leave_todos_as_none():
    mod, _ = load_module_capture()
    assert mod.key is not None, f"expected={True!r} actual={(mod.key is not None)!r}"
    assert mod.cache is not None, f"expected={True!r} actual={(mod.cache is not None)!r}"
    assert mod.key_hashable is not None, f"expected={True!r} actual={(mod.key_hashable is not None)!r}"


def test_cache_literal_contains_key_mapping_in_source():
    import pathlib

    path = pathlib.Path(__file__).resolve().parent / f"{MODULE_NAME}.py"
    if not path.exists():
        pytest.skip("module file not found next to tests")
    src = path.read_text(encoding="utf-8")

    tree = ast.parse(src)
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)]
    key_assign = next((a for a in assigns if any(isinstance(t, ast.Name) and t.id == "key" for t in a.targets)), None)
    cache_assign = next((a for a in assigns if any(isinstance(t, ast.Name) and t.id == "cache" for t in a.targets)), None)
    kh_assign = next((a for a in assigns if any(isinstance(t, ast.Name) and t.id == "key_hashable" for t in a.targets)), None)

    assert key_assign is not None, f"expected={True!r} actual={False!r}"
    assert cache_assign is not None, f"expected={True!r} actual={False!r}"
    assert kh_assign is not None, f"expected={True!r} actual={False!r}"

    assert not (isinstance(key_assign.value, ast.Constant) and key_assign.value.value is None), f"expected={True!r} actual={False!r}"
    assert not (isinstance(cache_assign.value, ast.Constant) and cache_assign.value.value is None), f"expected={True!r} actual={False!r}"
    assert not (isinstance(kh_assign.value, ast.Constant) and kh_assign.value.value is None), f"expected={True!r} actual={False!r}"