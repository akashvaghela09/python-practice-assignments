import importlib.util
import pathlib
import sys
import types
import pytest

MODULE_NAME = "06_complexNumbersBasics"
FILE_NAME = "06_complexNumbersBasics.py"


def load_module_from_path(tmp_path):
    src = pathlib.Path(__file__).resolve().parent / FILE_NAME
    if not src.exists():
        src = pathlib.Path(FILE_NAME)
    code = src.read_text(encoding="utf-8")
    target = tmp_path / FILE_NAME
    target.write_text(code, encoding="utf-8")

    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(target))
    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(MODULE_NAME, None)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_import_fails_before_fix(tmp_path):
    with pytest.raises(SyntaxError):
        load_module_from_path(tmp_path)


def test_expected_output_after_fix(tmp_path, capsys):
    src = pathlib.Path(__file__).resolve().parent / FILE_NAME
    if not src.exists():
        src = pathlib.Path(FILE_NAME)
    code = src.read_text(encoding="utf-8")

    fixed = (
        code.replace("real_part = __________", "real_part = z.real")
        .replace("imag_part = __________", "imag_part = z.imag")
        .replace("magnitude = __________  # use abs", "magnitude = abs(z)  # use abs")
    )

    spec = importlib.util.spec_from_loader(MODULE_NAME + "_fixed", loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(fixed, module.__dict__)

    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["3.0", "4.0", "5.0"], f"expected={['3.0','4.0','5.0']} actual={out}"