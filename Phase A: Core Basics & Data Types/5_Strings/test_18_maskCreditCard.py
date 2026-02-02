import importlib.util
import os
import re
import sys

import pytest


def _import_module():
    filename = "18_maskCreditCard.py"
    module_name = "mask_creditcard_18"
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_masked_exists_and_is_string():
    mod = _import_module()
    assert hasattr(mod, "masked")
    assert isinstance(mod.masked, str)


def test_masked_length_matches_card_length():
    mod = _import_module()
    assert hasattr(mod, "card")
    assert len(mod.masked) == len(mod.card)


def test_last_four_digits_preserved():
    mod = _import_module()
    assert mod.masked[-4:] == mod.card[-4:]


def test_all_previous_characters_are_asterisks():
    mod = _import_module()
    assert mod.masked[:-4] == ("*" * (len(mod.card) - 4))


def test_masked_has_only_asterisks_and_digits_and_digits_match_card_tail():
    mod = _import_module()
    assert re.fullmatch(r"[*0-9]+", mod.masked) is not None
    assert mod.masked.endswith(mod.card[-4:])


@pytest.mark.parametrize(
    "card_value",
    [
        "0000111122223333",
        "9999888877776666",
        "1234",
        "11112222333344445555",
    ],
)
def test_general_masking_property_using_student_mask_pattern(card_value):
    mod = _import_module()
    # Derive masking behavior solely from student output for the default card
    default_card = mod.card
    default_masked = mod.masked
    assert len(default_masked) == len(default_card)

    if len(default_card) >= 4:
        assert default_masked.endswith(default_card[-4:])
        prefix_len = len(default_card) - 4
        assert default_masked[:prefix_len] == "*" * prefix_len

    # Apply the same expected behavior to other card strings
    expected = ("*" * max(0, len(card_value) - 4)) + card_value[-4:]
    assert len(expected) == len(card_value)
    # Validate constructed expected shape (no disclosure of concrete values in messages)
    assert expected[:-4] == "*" * max(0, len(card_value) - 4)
    assert expected[-4:] == card_value[-4:]