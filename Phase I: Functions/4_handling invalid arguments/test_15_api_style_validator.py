import pytest
import importlib

mod = importlib.import_module("15_api_style_validator")
validate_payload = mod.validate_payload


def test_payload_must_be_dict():
    with pytest.raises(TypeError) as ei:
        validate_payload(["not", "a", "dict"])
    assert str(ei.value) == "payload must be a dict"


@pytest.mark.parametrize("missing_key", ["action", "data"])
def test_missing_required_keys(missing_key):
    payload = {"action": "create", "data": {"name": "Pen", "price": 1.5}}
    payload.pop(missing_key)
    with pytest.raises(KeyError) as ei:
        validate_payload(payload)
    assert str(ei.value) == repr(f"missing key: {missing_key}")


def test_no_extra_keys_allowed_in_payload():
    payload = {"action": "create", "data": {"name": "Pen", "price": 1.5}, "extra": 1}
    with pytest.raises(TypeError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "unexpected key: extra"


def test_action_must_be_valid():
    payload = {"action": "noop", "data": {}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid action"


def test_data_must_be_dict():
    payload = {"action": "create", "data": "nope"}
    with pytest.raises(TypeError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "data must be a dict"


def test_meta_optional_must_be_dict_when_present():
    payload = {"action": "create", "data": {"name": "Pen", "price": 1.5}, "meta": "x"}
    with pytest.raises(TypeError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "meta must be a dict"


def test_valid_create_returns_true():
    payload = {"action": "create", "data": {"name": "Pen", "price": 1.5}}
    assert validate_payload(payload) is True


@pytest.mark.parametrize(
    "bad_name",
    [None, "", "   ", 123, [], {}],
)
def test_create_invalid_name_raises_value_error(bad_name):
    payload = {"action": "create", "data": {"name": bad_name, "price": 1.5}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid name"


@pytest.mark.parametrize(
    "bad_price",
    [None, "1", 0, -1, -0.01, [], {}, True],
)
def test_create_invalid_price_raises_value_error(bad_price):
    payload = {"action": "create", "data": {"name": "Pen", "price": bad_price}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid price"


def test_create_missing_name_raises_invalid_name():
    payload = {"action": "create", "data": {"price": 1.5}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid name"


def test_create_missing_price_raises_invalid_price():
    payload = {"action": "create", "data": {"name": "Pen"}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid price"


def test_update_valid_id_only_returns_true():
    payload = {"action": "update", "data": {"id": 1}}
    assert validate_payload(payload) is True


@pytest.mark.parametrize("bad_id", [0, -1, None, "1", 1.2, True, [], {}])
def test_update_invalid_id_raises_value_error(bad_id):
    payload = {"action": "update", "data": {"id": bad_id}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid id"


def test_update_missing_id_raises_invalid_id():
    payload = {"action": "update", "data": {"name": "Pen"}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid id"


@pytest.mark.parametrize("bad_name", ["", "   ", 5, None])
def test_update_invalid_name_when_present_raises(bad_name):
    payload = {"action": "update", "data": {"id": 2, "name": bad_name}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid name"


@pytest.mark.parametrize("bad_price", [0, -1, "2", None, True])
def test_update_invalid_price_when_present_raises(bad_price):
    payload = {"action": "update", "data": {"id": 2, "price": bad_price}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid price"


def test_update_valid_name_and_price_returns_true():
    payload = {"action": "update", "data": {"id": 2, "name": "New", "price": 3.5}}
    assert validate_payload(payload) is True


def test_delete_valid_returns_true():
    payload = {"action": "delete", "data": {"id": 2}}
    assert validate_payload(payload) is True


@pytest.mark.parametrize("bad_id", [0, -1, None, "2", 2.2, True])
def test_delete_invalid_id_raises_value_error(bad_id):
    payload = {"action": "delete", "data": {"id": bad_id}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid id"


def test_delete_extra_data_keys_raises_invalid_data_keys():
    payload = {"action": "delete", "data": {"id": 2, "name": "x"}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid data keys"


def test_update_unexpected_data_key_raises_invalid_data_keys():
    payload = {"action": "update", "data": {"id": 1, "foo": "bar"}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid data keys"


def test_create_unexpected_data_key_raises_invalid_data_keys():
    payload = {"action": "create", "data": {"name": "Pen", "price": 1.5, "foo": 1}}
    with pytest.raises(ValueError) as ei:
        validate_payload(payload)
    assert str(ei.value) == "invalid data keys"


def test_payload_allows_meta_dict():
    payload = {
        "action": "create",
        "data": {"name": "Pen", "price": 1.5},
        "meta": {"request_id": "abc"},
    }
    assert validate_payload(payload) is True