import importlib.util
import os
import sys


def load_module(path, name="student_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_profile_exists_and_is_list(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_createMixedList.py")
    module = load_module(path)
    assert hasattr(module, "profile"), f"expected attribute exists=True actual exists={hasattr(module, 'profile')}"
    assert isinstance(module.profile, list), f"expected type=list actual type={type(module.profile).__name__}"


def test_profile_contents_and_order(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_createMixedList.py")
    module = load_module(path, name="student_module2")
    expected = ["Ava", 12, 4.5, True]
    assert module.profile == expected, f"expected value={expected!r} actual value={module.profile!r}"


def test_prints_profile(capsys):
    path = os.path.join(os.path.dirname(__file__), "03_createMixedList.py")
    module = load_module(path, name="student_module3")
    out = capsys.readouterr().out
    printed = [line for line in out.splitlines() if line.strip() != ""]
    assert printed, f"expected printed_lines>0 actual printed_lines={len(printed)}"
    last = printed[-1].strip()
    expected_last = str(module.profile)
    assert last == expected_last, f"expected last_line={expected_last!r} actual last_line={last!r}"