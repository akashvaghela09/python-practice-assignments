# Unpack a tuple while ignoring unwanted values using underscores.

record = ("order-17", "2026-02-01", "PAID", 49.99)

# TODO: unpack into order_id and amount only, ignoring the date and status

print(order_id)
print(amount)
# Expected outcome:
# order-17
# 49.99
