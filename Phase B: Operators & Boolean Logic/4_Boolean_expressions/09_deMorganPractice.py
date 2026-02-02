# Goal: Use De Morgan's laws to create equivalent boolean expressions.
# Expected outcome:
# It prints exactly:
# original: False
# equivalent: False
# match: True

is_hungry = True
has_food = True
has_time = False

# original means: NOT (has_food AND has_time)
original = ???

# equivalent should be written WITHOUT a leading NOT applied to parentheses.
# Use only 'not' directly on variables and 'and'/'or'.
equivalent = ???

match = (original == equivalent)

print("original:", original)
print("equivalent:", equivalent)
print("match:", match)
