import importlib
import sys
import types


def _load_module_with_capture(module_name, file_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

    captured = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        captured.append(sep.join(str(a) for a in args) + ("" if end == "" else end))

    mod = types.ModuleType(module_name)
    mod.__file__ = file_name
    mod.__dict__["print"] = fake_print

    with open(file_name, "r", encoding="utf-8") as f:
        code = f.read()

    exec(compile(code, file_name, "exec"), mod.__dict__)
    sys.modules[module_name] = mod
    output = "".join(captured)
    return mod, output


def test_printed_output_exact():
    _, out = _load_module_with_capture("assignment_02_membership", "02_membershipBasics_lists.py")
    actual_lines = out.splitlines()
    expected_lines = ["True", "True", "False"]
    assert actual_lines == expected_lines, f"expected={expected_lines} actual={actual_lines}"


def test_numbers_list_unchanged():
    mod, _ = _load_module_with_capture("assignment_02_membership_numbers", "02_membershipBasics_lists.py")
    assert hasattr(mod, "numbers"), f"expected={'numbers variable to exist'} actual={getattr(mod, 'numbers', None)}"
    assert isinstance(mod.numbers, list), f"expected={list} actual={type(mod.numbers)}"
    expected = [2, 4, 6, 8]
    assert mod.numbers == expected, f"expected={expected} actual={mod.numbers}"


def test_no_extra_stdout_whitespace():
    _, out = _load_module_with_capture("assignment_02_membership_ws", "02_membershipBasics_lists.py")
    assert out == "True\nTrue\nFalse\n", f"expected={'True\\nTrue\\nFalse\\n'} actual={out!r}"