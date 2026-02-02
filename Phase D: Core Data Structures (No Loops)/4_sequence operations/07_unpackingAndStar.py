# Task: Use sequence unpacking (including starred unpacking).
# Expected outcome:
# - first should be 'red'
# - middle should be ['green', 'blue']
# - last should be 'yellow'

colors = ["red", "green", "blue", "yellow"]

first, *middle, last = __

print(first)
print(middle)
print(last)
