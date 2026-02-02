# Goal: Calculate ticket price with age and time-based pricing.
# Rules:
# - If age < 0 -> print "Invalid age"
# - Else determine base price:
#     - age <= 12 -> 8
#     - age <= 64 -> 12
#     - else -> 9
# - Then apply time discount:
#     - if show_time is "matinee" -> subtract 2 from base price
#     - elif show_time is "evening" -> no change
#     - else -> print "Invalid show time" (and do not print a price)
# Expected outcome for age=70, show_time="matinee": Ticket price: 7

age = 70
show_time = "matinee"  # "matinee" or "evening"

# TODO: Use if/elif/else to print exactly:
# "Invalid age" OR "Invalid show time" OR "Ticket price: <number>"

