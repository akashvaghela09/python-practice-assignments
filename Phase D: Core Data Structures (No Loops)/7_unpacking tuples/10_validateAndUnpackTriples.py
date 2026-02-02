# Each item should be a 3-tuple: (product, qty, unit_price).
# Unpack each triple, compute line totals, and compute the grand total.
# If any item is not length 3, skip it.

items = [
    ("pen", 3, 1.50),
    ("notebook", 2, 4.00),
    ("bad-item", 9),
    ("eraser", 1, 0.75)
]

line_totals = []
grand_total = 0.0

# TODO:
# - Loop through items
# - If the tuple does not have exactly 3 elements, continue
# - Otherwise unpack into product, qty, unit_price
# - Compute total = qty * unit_price
# - Append (product, total) to line_totals
# - Add total to grand_total

print(line_totals)
print(f"{grand_total:.2f}")
# Expected outcome:
# [('pen', 4.5), ('notebook', 8.0), ('eraser', 0.75)]
# 13.25
