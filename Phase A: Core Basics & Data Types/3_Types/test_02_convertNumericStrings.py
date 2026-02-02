import importlib.util
import sys
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("student_mod", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["student_mod"] = module
    spec.loader.exec_module(module)
    return module


def test_module_imports_without_syntax_error():
    path = Path(__file__).resolve().parent / "02_convertNumericStrings.py"
    load_module(path)


def test_conversions_and_output(capsys):
    path = Path(__file__).resolve().parent / "02_convertNumericStrings.py"
    mod = load_module(path)
    captured = capsys.readouterr().out

    assert hasattr(mod, "n1")
    assert hasattr(mod, "n2")

    expected_n1 = int(mod.s1)
    expected_n2 = float(mod.s2)

    assert mod.n1 == expected_n1, f"expected={expected_n1!r} actual={mod.n1!r}"
    assert mod.n2 == expected_n2, f"expected={expected_n2!r} actual={mod.n2!r}"

    expected_out = f"{expected_n1}\n{expected_n2}\n"
    assert captured == expected_out, f"expected={expected_out!r} actual={captured!r}"