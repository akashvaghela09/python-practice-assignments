import importlib.util
import pathlib
import re
import sys
import pytest


def _load_module_from_path(path):
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_assignment_path():
    return pathlib.Path(__file__).resolve().parent / "08_collatzSteps.py"


def test_file_exists():
    p = _get_assignment_path()
    assert p.exists()


def test_no_placeholders_remaining():
    p = _get_assignment_path()
    text = p.read_text(encoding="utf-8")
    assert "__________" not in text


def test_import_executes_without_syntax_error_or_hang(capsys):
    p = _get_assignment_path()
    module = _load_module_from_path(p)
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) >= 1
    assert out[-1].startswith("Steps:")


def test_printed_steps_matches_steps_variable(capsys):
    p = _get_assignment_path()
    module = _load_module_from_path(p)
    out = capsys.readouterr().out.strip().splitlines()
    last = out[-1].strip()
    m = re.match(r"^Steps:\s*(-?\d+)\s*$", last)
    assert m is not None
    printed = int(m.group(1))
    assert hasattr(module, "steps")
    assert printed == module.steps


def test_module_variables_types_and_values_consistent(capsys):
    p = _get_assignment_path()
    module = _load_module_from_path(p)
    _ = capsys.readouterr()
    assert hasattr(module, "n")
    assert hasattr(module, "steps")
    assert isinstance(module.steps, int)
    assert isinstance(module.n, int)
    assert module.n == 1
    assert module.steps >= 0


@pytest.mark.parametrize(
    "start_n",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 27, 97, 871, 6171],
)
def test_algorithm_correct_for_various_inputs_without_hardcoding(start_n):
    p = _get_assignment_path()
    text = p.read_text(encoding="utf-8")

    patched = re.sub(r"^\s*n\s*=\s*6\s*$", f"n = {start_n}", text, flags=re.M)
    assert patched != text  # ensure we actually changed the starting n
    patched = re.sub(r"print\((.*)\)", r"# removed print(\1)", patched, count=1)

    ns = {}
    exec(compile(patched, str(p), "exec"), ns, ns)

    def ref_steps(n):
        steps = 0
        while n != 1:
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            steps += 1
        return steps

    expected = ref_steps(start_n)
    actual = ns.get("steps")
    assert actual == expected


def test_uses_while_loop_and_modulo_parity_check():
    p = _get_assignment_path()
    text = p.read_text(encoding="utf-8")
    assert re.search(r"\bwhile\b", text) is not None
    assert re.search(r"%\s*2", text) is not None


def test_steps_increment_present():
    p = _get_assignment_path()
    text = p.read_text(encoding="utf-8")
    assert re.search(r"\bsteps\s*=\s*steps\s*\+\s*1\b|\bsteps\s*\+=\s*1\b", text) is not None