import importlib.util
import pathlib


def _load_module():
    path = pathlib.Path(__file__).resolve().parent / "10_sequenceWindowMaxSum.py"
    spec = importlib.util.spec_from_file_location("seqwinmaxsum_mod", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_max_sum_value_matches_expected():
    m = _load_module()
    expected = max(sum(m.data[i : i + m.k]) for i in range(0, len(m.data) - m.k + 1))
    assert m.max_sum == expected, f"expected={expected} actual={m.max_sum}"


def test_max_sum_is_int():
    m = _load_module()
    assert isinstance(m.max_sum, int), f"expected={int} actual={type(m.max_sum)}"


def test_max_sum_changes_with_modified_data_and_k():
    m = _load_module()

    m.data = [10, -1, -1, -1]
    m.k = 2

    expected = max(sum(m.data[i : i + m.k]) for i in range(0, len(m.data) - m.k + 1))

    assert m.max_sum != expected, f"expected_not={expected} actual={m.max_sum}"


def test_handles_all_negative_numbers():
    m = _load_module()

    m.data = [-5, -2, -3, -4]
    m.k = 2
    expected = max(sum(m.data[i : i + m.k]) for i in range(0, len(m.data) - m.k + 1))

    assert expected == -5
    assert m.max_sum != expected, f"expected_not={expected} actual={m.max_sum}"