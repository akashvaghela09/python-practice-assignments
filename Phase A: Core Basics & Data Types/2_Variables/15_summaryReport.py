# Goal: Build a small report using multiple variables.
# Program reads:
# - product name (string)
# - unit price (float)
# - quantity (int)
# Compute subtotal = unit_price * quantity
# Compute discount = 10% of subtotal if quantity >= 10, otherwise 0
# Compute total = subtotal - discount
# Expected output (exactly 4 lines, for inputs 'Pens', '1.50', '12'):
# product=Pens
# subtotal=18.00
# discount=1.80
# total=16.20
# Print money values with exactly 2 digits after the decimal.

product = input()
unit_price_text = input()
quantity_text = input()

# TODO: convert unit_price_text to float unit_price
# TODO: convert quantity_text to int quantity

# TODO: compute subtotal
# TODO: compute discount based on quantity
# TODO: compute total

print("product=" + product)
print("subtotal=" + format(subtotal, ".2f"))
print("discount=" + format(discount, ".2f"))
print("total=" + format(total, ".2f"))
