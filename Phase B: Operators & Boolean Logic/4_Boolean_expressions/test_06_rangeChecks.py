import importlib.util
import pathlib
import sys


def _load_module(path):
    module_name = pathlib.Path(path).stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_module_imports_without_syntax_error():
    import 06_rangeChecks  # noqa: F401


def test_expected_output(capsys):
    import 06_rangeChecks  # noqa: F401
    captured = capsys.readouterr()
    actual = captured.out
    expected = (
        "in_range_1_to_10: True\n"
        "is_weekend_day: False\n"
        "valid_percentage: True\n"
    )
    assert actual == expected, f"expected={expected!r} actual={actual!r}"


def test_variables_are_booleans():
    import 06_rangeChecks as m

    assert isinstance(m.in_range_1_to_10, bool), f"expected={bool!r} actual={type(m.in_range_1_to_10)!r}"
    assert isinstance(m.is_weekend_day, bool), f"expected={bool!r} actual={type(m.is_weekend_day)!r}"
    assert isinstance(m.valid_percentage, bool), f"expected={bool!r} actual={type(m.valid_percentage)!r}"


def test_logic_generalizes_by_reexecuting_with_modified_inputs(tmp_path):
    src_path = pathlib.Path(__file__).with_name("06_rangeChecks.py")
    code = src_path.read_text(encoding="utf-8")

    def run_case(x, weekday, pct):
        patched = code
        patched = patched.replace("x = 7", f"x = {x}")
        patched = patched.replace('weekday = "Wed"', f'weekday = "{weekday}"')
        patched = patched.replace("pct = 100", f"pct = {pct}")

        case_path = tmp_path / f"case_{x}_{weekday}_{pct}.py"
        case_path.write_text(patched, encoding="utf-8")
        mod = _load_module(str(case_path))
        return mod.in_range_1_to_10, mod.is_weekend_day, mod.valid_percentage

    assert run_case(1, "Sat", 0) == (True, True, True)
    assert run_case(10, "Sun", 100) == (True, True, True)
    assert run_case(0, "Mon", -1) == (False, False, False)
    assert run_case(11, "Fri", 101) == (False, False, False)
    assert run_case(5, "Tue", 50) == (True, False, True)