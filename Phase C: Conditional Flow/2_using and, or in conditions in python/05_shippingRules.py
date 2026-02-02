# Goal: Determine shipping type.
# Rules:
# - FREE if (cart_total >= 50 AND is_domestic) OR is_premium_member
# - Otherwise STANDARD
# Expected outcome:
# With cart_total=45, is_domestic=True, is_premium_member=True => print exactly: FREE
# With cart_total=45, is_domestic=True, is_premium_member=False => print exactly: STANDARD

cart_total = 45
is_domestic = True
is_premium_member = True

# TODO: Implement the FREE/ STANDARD decision.
if ____:
    print("FREE")
else:
    print("STANDARD")
