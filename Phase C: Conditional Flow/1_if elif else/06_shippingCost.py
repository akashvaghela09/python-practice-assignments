# Goal: Compute shipping cost based on weight and membership.
# Rules:
# - If weight <= 0 -> print "Invalid weight"
# - Else if member is True:
#     - weight <= 2 -> cost 0
#     - weight <= 5 -> cost 3
#     - else -> cost 7
# - Else (non-member):
#     - weight <= 2 -> cost 5
#     - weight <= 5 -> cost 8
#     - else -> cost 12
# Expected outcome for weight=4.5, member=False: Shipping cost: 8

weight = 4.5
member = False

# TODO: Use if/elif/else to print either:
# "Invalid weight" OR "Shipping cost: <number>"

