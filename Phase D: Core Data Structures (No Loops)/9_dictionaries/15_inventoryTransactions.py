# Goal: Process transactions to update an inventory dictionary.
# Rules:
# - inventory maps item -> quantity
# - each transaction is a dict with keys: "item", "delta"
# - if an item doesn't exist yet, treat its starting quantity as 0
# - after applying all transactions, remove any items with quantity == 0
# Expected outcome when run:
# {'apple': 2, 'orange': 4}

inventory = {"apple": 1, "orange": 3}
transactions = [
    {"item": "apple", "delta": 3},
    {"item": "orange", "delta": 1},
    {"item": "banana", "delta": 2},
    {"item": "banana", "delta": -2},
    {"item": "apple", "delta": -2}
]

# TODO: apply transactions to inventory
# TODO: remove zero-quantity items

print(inventory)
