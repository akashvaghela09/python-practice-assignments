# Goal: Combine numeric operators to compute a discounted total with tax.
# Rules:
# - subtotal = price * qty
# - discount_amount = subtotal * (discount_percent / 100)
# - after_discount = subtotal - discount_amount
# - tax_amount = after_discount * (tax_percent / 100)
# - final_total = after_discount + tax_amount
# - final_total should be rounded to 2 decimals using round(final_total, 2)
# Expected outcome: When run, the program prints exactly:
# Final total: 91.07

price = 19.99
qty = 4
discount_percent = 10
tax_percent = 8.25

# TODO: compute final_total following the rules above
final_total = None

print("Final total:", final_total)
