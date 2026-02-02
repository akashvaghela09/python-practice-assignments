import importlib.util
import sys
from pathlib import Path


def _run_module_capture_stdout(module_filename, capsys):
    module_path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(module_filename[:-3], module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    out = capsys.readouterr().out
    return module, out


def test_output_exact(capsys):
    _, out = _run_module_capture_stdout("02_comparisonsWithVariables.py", capsys)
    expected = "is_adult: True\nis_senior: False\nis_teen: False\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_variables_are_booleans_and_values(capsys):
    module, _ = _run_module_capture_stdout("02_comparisonsWithVariables.py", capsys)

    assert hasattr(module, "age"), "expected=True actual=False"
    assert hasattr(module, "is_adult"), "expected=True actual=False"
    assert hasattr(module, "is_senior"), "expected=True actual=False"
    assert hasattr(module, "is_teen"), "expected=True actual=False"

    assert module.age == 20, f"expected={20!r} actual={module.age!r}"

    assert isinstance(module.is_adult, bool), f"expected={bool!r} actual={type(module.is_adult)!r}"
    assert isinstance(module.is_senior, bool), f"expected={bool!r} actual={type(module.is_senior)!r}"
    assert isinstance(module.is_teen, bool), f"expected={bool!r} actual={type(module.is_teen)!r}"

    assert module.is_adult is True, f"expected={True!r} actual={module.is_adult!r}"
    assert module.is_senior is False, f"expected={False!r} actual={module.is_senior!r}"
    assert module.is_teen is False, f"expected={False!r} actual={module.is_teen!r}"


def test_no_placeholder_left_in_source():
    module_path = Path(__file__).resolve().parent / "02_comparisonsWithVariables.py"
    src = module_path.read_text(encoding="utf-8")
    assert "???" not in src, f"expected={False!r} actual={('???' in src)!r}"