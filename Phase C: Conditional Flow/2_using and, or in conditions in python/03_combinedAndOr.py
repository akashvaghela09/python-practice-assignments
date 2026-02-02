# Goal: Decide if a discount applies.
# Rule: discount applies if (is_student AND age < 26) OR is_veteran
# Expected outcome:
# With is_student=True, age=20, is_veteran=False => print exactly: DISCOUNT
# If you change age to 30 (keeping others the same) => print exactly: NO DISCOUNT

is_student = True
age = 20
is_veteran = False

# TODO: Fill in the combined condition using 'and' and 'or'.
if ____:
    print("DISCOUNT")
else:
    print("NO DISCOUNT")
