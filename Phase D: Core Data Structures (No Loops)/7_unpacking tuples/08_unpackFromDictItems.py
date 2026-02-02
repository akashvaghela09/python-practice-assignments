# Iterate over dict items and unpack key/value pairs. Build a comma-separated summary.

prices = {"apple": 1.25, "banana": 0.75, "cherry": 2.5}

parts = []
# TODO: iterate over prices.items(), unpack into name and price, append "name=price" with exact formatting below
# Formatting rules:
# - Use exactly two decimal places for the price
# - Keep the iteration order as given by the literal

summary = ", ".join(parts)
print(summary)
# Expected outcome:
# apple=1.25, banana=0.75, cherry=2.50
