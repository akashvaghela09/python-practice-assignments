import importlib.util
import os
import sys
import subprocess
import re
import pytest

MODULE_FILE = "15_frozenSetAsDictionaryKey.py"


def _run_script(path):
    return subprocess.run(
        [sys.executable, path],
        capture_output=True,
        text=True,
    )


def test_script_runs_and_prints_3(tmp_path):
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    assert os.path.exists(src_path)

    res = _run_script(src_path)

    assert res.returncode == 0, f"expected=0 actual={res.returncode}"
    out = res.stdout.strip()
    assert re.fullmatch(r"\s*3\s*", out) is not None, f"expected='3' actual={res.stdout!r}"
    assert res.stderr.strip() == "", f"expected='' actual={res.stderr!r}"


def test_import_has_groups_len_3_and_valid_grouping():
    src_path = os.path.join(os.path.dirname(__file__), MODULE_FILE)
    spec = importlib.util.spec_from_file_location("mod15", src_path)
    mod = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(mod)

    assert hasattr(mod, "groups")
    groups = mod.groups

    assert isinstance(groups, dict), f"expected=dict actual={type(groups).__name__}"
    assert len(groups) == 3, f"expected=3 actual={len(groups)}"

    all_words = []
    for k, v in groups.items():
        assert isinstance(v, list), f"expected=list actual={type(v).__name__}"
        all_words.extend(v)

        if isinstance(k, (frozenset, tuple)):
            pass
        else:
            assert False, f"expected=frozenset_or_tuple actual={type(k).__name__}"

        for word in v:
            if isinstance(k, tuple):
                assert tuple(sorted(word)) == k, f"expected={k} actual={tuple(sorted(word))}"
            else:
                assert frozenset(word) == k, f"expected={k} actual={frozenset(word)}"

    assert sorted(all_words) == sorted(mod.words), f"expected={sorted(mod.words)} actual={sorted(all_words)}"
    assert len(all_words) == len(mod.words), f"expected={len(mod.words)} actual={len(all_words)}"