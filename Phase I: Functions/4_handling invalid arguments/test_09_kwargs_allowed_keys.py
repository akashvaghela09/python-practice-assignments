import pytest

from 09_kwargs_allowed_keys import build_query


def test_build_query_valid_only_q():
    assert build_query(q="cats") == {"q": "cats"}


def test_build_query_valid_q_page():
    assert build_query(q="cats", page=1) == {"q": "cats", "page": 1}


def test_build_query_valid_all_keys():
    assert build_query(q="cats", page=2, limit=10) == {"q": "cats", "page": 2, "limit": 10}


def test_build_query_ignores_not_provided_keys():
    assert build_query(page=3) == {"page": 3}


@pytest.mark.parametrize("bad_key", ["sort", "offset", "q ", "Page", "__proto__"])
def test_build_query_unexpected_parameter_raises_typeerror(bad_key):
    with pytest.raises(TypeError) as ei:
        build_query(**{bad_key: "x"})
    assert str(ei.value) == f"unexpected parameter: {bad_key}"


@pytest.mark.parametrize("q_value", ["", "   ", "\n\t  "])
def test_build_query_q_empty_after_strip_raises(q_value):
    with pytest.raises(ValueError) as ei:
        build_query(q=q_value)
    assert str(ei.value) == "q must be a non-empty string"


@pytest.mark.parametrize("q_value", [None, 123, 12.3, [], {}, object()])
def test_build_query_q_non_string_raises(q_value):
    with pytest.raises(ValueError) as ei:
        build_query(q=q_value)
    assert str(ei.value) == "q must be a non-empty string"


def test_build_query_q_does_not_strip_value_when_returning():
    assert build_query(q="  cats  ") == {"q": "  cats  "}


@pytest.mark.parametrize("page_value", [0, -1, -10])
def test_build_query_page_non_positive_int_raises(page_value):
    with pytest.raises(ValueError) as ei:
        build_query(page=page_value)
    assert str(ei.value) == "page must be a positive int"


@pytest.mark.parametrize("page_value", [True, False])
def test_build_query_page_bool_not_allowed(page_value):
    with pytest.raises(ValueError) as ei:
        build_query(page=page_value)
    assert str(ei.value) == "page must be a positive int"


@pytest.mark.parametrize("page_value", [1.0, "1", None, [], {}, object()])
def test_build_query_page_non_int_raises(page_value):
    with pytest.raises(ValueError) as ei:
        build_query(page=page_value)
    assert str(ei.value) == "page must be a positive int"


@pytest.mark.parametrize("limit_value", [0, -1, -5])
def test_build_query_limit_non_positive_int_raises(limit_value):
    with pytest.raises(ValueError) as ei:
        build_query(limit=limit_value)
    assert str(ei.value) == "limit must be a positive int"


@pytest.mark.parametrize("limit_value", [True, False])
def test_build_query_limit_bool_not_allowed(limit_value):
    with pytest.raises(ValueError) as ei:
        build_query(limit=limit_value)
    assert str(ei.value) == "limit must be a positive int"


@pytest.mark.parametrize("limit_value", [1.0, "10", None, [], {}, object()])
def test_build_query_limit_non_int_raises(limit_value):
    with pytest.raises(ValueError) as ei:
        build_query(limit=limit_value)
    assert str(ei.value) == "limit must be a positive int"


def test_build_query_returns_new_dict_not_same_reference():
    out = build_query(q="cats", page=1)
    assert out == {"q": "cats", "page": 1}
    out["page"] = 999
    assert build_query(q="cats", page=1) == {"q": "cats", "page": 1}