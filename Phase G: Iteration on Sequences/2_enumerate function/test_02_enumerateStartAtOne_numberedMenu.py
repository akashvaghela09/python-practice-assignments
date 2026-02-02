import importlib.util
import pathlib
import re
import sys


def _load_module(path):
    name = pathlib.Path(path).stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_output_matches_expected(capsys):
    path = pathlib.Path(__file__).resolve().parent / "02_enumerateStartAtOne_numberedMenu.py"
    _load_module(str(path))
    captured = capsys.readouterr()
    out_lines = [line.rstrip("\n") for line in captured.out.splitlines() if line.strip() != ""]
    expected = ["1 - Home", "2 - Settings", "3 - Logout"]
    assert expected == out_lines, f"expected={expected!r} actual={out_lines!r}"


def test_uses_enumerate_with_start_1():
    path = pathlib.Path(__file__).resolve().parent / "02_enumerateStartAtOne_numberedMenu.py"
    src = path.read_text(encoding="utf-8")
    src_nocomments = "\n".join([line for line in src.splitlines() if not line.lstrip().startswith("#")])
    pattern = re.compile(r"enumerate\s*\(\s*items\s*,\s*start\s*=\s*1\s*\)")
    found = bool(pattern.search(src_nocomments))
    assert found, f"expected={True!r} actual={found!r}"


def test_no_hardcoded_numbered_strings_in_source():
    path = pathlib.Path(__file__).resolve().parent / "02_enumerateStartAtOne_numberedMenu.py"
    src = path.read_text(encoding="utf-8")
    src_nocomments = "\n".join([line for line in src.splitlines() if not line.lstrip().startswith("#")])
    hardcoded = bool(re.search(r"(['\"])1\s*-\s*Home\1|(['\"])2\s*-\s*Settings\2|(['\"])3\s*-\s*Logout\2", src_nocomments))
    assert hardcoded is False, f"expected={False!r} actual={hardcoded!r}"