# Task: Build a small pricing engine using functions calling functions.
# Implement:
# - subtotal(prices): returns sum of list
# - discount_amount(subtotal_value, percent): percent is like 10 for 10%
# - tax_amount(amount, percent): same percent format
# - final_total(prices, discount_percent, tax_percent):
#     1) compute sub = subtotal(prices)
#     2) compute disc = discount_amount(sub, discount_percent)
#     3) compute after_discount = sub - disc
#     4) compute tax = tax_amount(after_discount, tax_percent)
#     5) return after_discount + tax
# Expected outcome: print(final_total([20, 5], 10, 8)) outputs exactly: 24.3
# Note: Use normal float arithmetic; do not round.

def subtotal(prices):
    # TODO
    pass


def discount_amount(subtotal_value, percent):
    # TODO
    pass


def tax_amount(amount, percent):
    # TODO
    pass


def final_total(prices, discount_percent, tax_percent):
    # TODO: call the helpers in the specified order
    pass


print(final_total([20, 5], 10, 8))
