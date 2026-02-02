import importlib.util
import pathlib


def load_and_capture_output(module_filename, monkeypatch):
    outputs = []

    def fake_print(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        outputs.append(sep.join(str(a) for a in args) + end)

    monkeypatch.setattr("builtins.print", fake_print)
    path = pathlib.Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(module_filename, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return "".join(outputs)


def test_prints_exact_result_pass(monkeypatch):
    out = load_and_capture_output("06_ternary_with_string_formatting.py", monkeypatch)
    expected = "Result: PASS\n"
    assert out == expected, f"expected={expected!r} actual={out!r}"


def test_no_extra_output(monkeypatch):
    out = load_and_capture_output("06_ternary_with_string_formatting.py", monkeypatch)
    expected_lines = ["Result: PASS"]
    actual_lines = out.splitlines()
    assert actual_lines == expected_lines, f"expected={expected_lines!r} actual={actual_lines!r}"