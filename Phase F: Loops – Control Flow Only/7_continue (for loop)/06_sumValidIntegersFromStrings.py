# Sum only the items that can be converted to int from the list below.
# Use a for loop and continue to skip invalid items (non-integer strings).
# Print the final sum.
# Expected outcome (exact):
# 15

items = ["10", "-3", "x", " 5 ", "7.2", "3"]

total = 0
for s in items:
    s = s.strip()
    # TODO: attempt int conversion; if it fails, continue
    # Hint: use try/except
    
    # TODO: add the integer to total
    
print(total)
