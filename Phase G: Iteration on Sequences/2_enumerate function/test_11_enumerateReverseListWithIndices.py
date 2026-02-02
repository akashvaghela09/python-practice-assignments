import importlib.util
import pathlib
import sys
import pytest


MODULE_NAME = "11_enumerateReverseListWithIndices"
FILE_NAME = "11_enumerateReverseListWithIndices.py"


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / FILE_NAME
    spec = importlib.util.spec_from_file_location(MODULE_NAME, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def test_prints_reverse_with_original_indices(capsys):
    _load_module()
    out = capsys.readouterr().out
    expected = "3 d\n2 c\n1 b\n0 a\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_letters_unchanged():
    mod = _load_module()
    assert hasattr(mod, "letters")
    assert mod.letters == ["a", "b", "c", "d"]


@pytest.mark.parametrize(
    "bad",
    [
        "d 3\nc 2\nb 1\na 0\n",
        "0 d\n1 c\n2 b\n3 a\n",
        "3 d\r\n2 c\r\n1 b\r\n0 a\r\n",
        "3 d\n2 c\n1 b\n0 a",
    ],
)
def test_output_not_common_mistakes(capsys, bad):
    _load_module()
    out = capsys.readouterr().out
    assert out != bad, f"expected={bad!r} actual={out!r}"