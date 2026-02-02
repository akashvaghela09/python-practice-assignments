# Goal: Count how many orders require manual review.
# Manual review rules:
# - (amount > 1000 AND is_international) OR
# - (amount > 2000) OR
# - (is_flagged AND amount > 100)
# Expected outcome:
# For the provided orders list, print exactly: MANUAL REVIEW COUNT: 3

orders = [
    {"id": 1, "amount": 1500, "is_international": True,  "is_flagged": False},
    {"id": 2, "amount": 900,  "is_international": True,  "is_flagged": False},
    {"id": 3, "amount": 2500, "is_international": False, "is_flagged": False},
    {"id": 4, "amount": 120,  "is_international": False, "is_flagged": True},
    {"id": 5, "amount": 80,   "is_international": False, "is_flagged": True},
    {"id": 6, "amount": 1100, "is_international": False, "is_flagged": False}
]

count = 0
for order in orders:
    amount = order["amount"]
    is_international = order["is_international"]
    is_flagged = order["is_flagged"]

    # TODO: Write the condition for manual review using 'and'/'or'.
    if ____:
        count += 1

print(f"MANUAL REVIEW COUNT: {count}")
