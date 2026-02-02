import importlib.util
import sys
from pathlib import Path


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_placeholders_left():
    p = Path(__file__).resolve().parent / "08_subsetSupersetChecks.py"
    src = p.read_text(encoding="utf-8")
    assert "____" not in src, f"expected placeholder removed vs actual found"


def test_output_lines(capsys):
    p = Path(__file__).resolve().parent / "08_subsetSupersetChecks.py"
    mod_name = "subset_superset_checks_08"
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    _load_module(mod_name, p)
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["True", "False", "True"], f"expected {['True','False','True']} vs actual {out}"