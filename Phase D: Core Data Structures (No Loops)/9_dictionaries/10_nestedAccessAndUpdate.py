# Goal: Access and update nested dictionary data.
# Expected outcome when run:
# 94110
# {'name': 'Riley', 'address': {'city': 'SF', 'zip': '94110'}, 'visits': 3}

customer = {
    "name": "Riley",
    "address": {"city": "SF", "zip": "94107"},
    "visits": 2
}

# TODO: print the zip code
# TODO: update zip to "94110"
# TODO: increment visits by 1

print(customer["address"]["zip"])
print(customer)
