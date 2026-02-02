import importlib.util
import pathlib
import sys


def _load_module(tmp_path):
    src = pathlib.Path(__file__).with_name("10_subsequence_search_in_2d.py")
    dst = tmp_path / "mod_10_subsequence_search_in_2d.py"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("mod_10_subsequence_search_in_2d", str(dst))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_printed_output_exact(capsys, tmp_path):
    _load_module(tmp_path)
    out = capsys.readouterr().out
    expected = "available: ['A1', 'B4']\nunavailable: ['A2', 'C3']\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_valid_seats_set_built(tmp_path, capsys):
    mod = _load_module(tmp_path)
    capsys.readouterr()

    expected_valid = {f"{r}{c}" for r in ["A", "B", "C"] for c in [1, 2, 3, 4]}
    actual_valid = getattr(mod, "valid_seats", None)
    assert actual_valid == expected_valid, f"expected={expected_valid!r} actual={actual_valid!r}"


def test_available_unavailable_lists(tmp_path, capsys):
    mod = _load_module(tmp_path)
    capsys.readouterr()

    expected_available = ["A1", "B4"]
    expected_unavailable = ["A2", "C3"]

    assert getattr(mod, "available", None) == expected_available, (
        f"expected={expected_available!r} actual={getattr(mod, 'available', None)!r}"
    )
    assert getattr(mod, "unavailable", None) == expected_unavailable, (
        f"expected={expected_unavailable!r} actual={getattr(mod, 'unavailable', None)!r}"
    )