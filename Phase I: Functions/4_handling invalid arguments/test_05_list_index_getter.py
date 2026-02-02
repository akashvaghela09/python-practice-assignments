import pytest
import importlib.util
from pathlib import Path

# --- dynamic import for numbered module ---
MODULE_PATH = Path(__file__).parent / "05_list_index_getter.py"

spec = importlib.util.spec_from_file_location("list_index_getter_05", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

get_item_at = module.get_item_at
# -----------------------------------------


def test_returns_item_from_list():
    seq = ["a", "b", "c"]
    index = 1
    expected = seq[index]
    actual = get_item_at(seq, index)
    assert actual == expected, f"expected {expected!r} but got {actual!r}"


def test_returns_item_from_tuple():
    seq = (10, 20, 30)
    index = 2
    expected = seq[index]
    actual = get_item_at(seq, index)
    assert actual == expected, f"expected {expected!r} but got {actual!r}"


def test_negative_index_supported_like_python():
    seq = ["x", "y", "z"]
    index = -1
    expected = seq[index]
    actual = get_item_at(seq, index)
    assert actual == expected, f"expected {expected!r} but got {actual!r}"


@pytest.mark.parametrize("seq", ["abc", {"a": 1}, {"a", "b"}, 123, 12.3, object(), None])
def test_seq_must_be_list_or_tuple(seq):
    with pytest.raises(TypeError) as ei:
        get_item_at(seq, 0)
    assert str(ei.value) == "seq must be a list or tuple", (
        f"expected {'seq must be a list or tuple'!r} but got {str(ei.value)!r}"
    )


@pytest.mark.parametrize("index", [0.0, 1.5, "1", None, [], {}, (1,), object()])
def test_index_must_be_int(index):
    with pytest.raises(TypeError) as ei:
        get_item_at([1, 2, 3], index)
    assert str(ei.value) == "index must be an int", (
        f"expected {'index must be an int'!r} but got {str(ei.value)!r}"
    )


@pytest.mark.parametrize("index", [True, False])
def test_index_bool_not_allowed(index):
    with pytest.raises(TypeError) as ei:
        get_item_at([1, 2, 3], index)
    assert str(ei.value) == "index must be an int", (
        f"expected {'index must be an int'!r} but got {str(ei.value)!r}"
    )


@pytest.mark.parametrize(
    "seq,index",
    [([1], 1), ([1], 2), ([], 0), (("a",), 5), (("a", "b"), -3)],
)
def test_index_out_of_range_raises_indexerror(seq, index):
    with pytest.raises(IndexError) as ei:
        get_item_at(seq, index)
    assert str(ei.value) == "index out of range", (
        f"expected {'index out of range'!r} but got {str(ei.value)!r}"
    )


def test_errors_order_seq_checked_before_index():
    with pytest.raises(TypeError) as ei:
        get_item_at("not a sequence", "0")
    assert str(ei.value) == "seq must be a list or tuple", (
        f"expected {'seq must be a list or tuple'!r} but got {str(ei.value)!r}"
    )
