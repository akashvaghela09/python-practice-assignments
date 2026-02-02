# Goal: Use Decimal for money to avoid float issues.
# Expected outcome (exact lines):
# 0.3
# 0.30
# 3.50

from decimal import Decimal, getcontext

getcontext().prec = 28

a = Decimal("0.1")
b = Decimal("0.2")

sum_ab = __________

# Print sum_ab as a plain number (should show 0.3)
print(sum_ab)

# Print sum_ab with exactly two decimal places
print(__________)  # use quantize

price = Decimal("1.75")
qty = 2

# Compute total cost as Decimal and print with two decimals (3.50)
total_cost = __________
print(__________)  # quantize to 2 decimals
