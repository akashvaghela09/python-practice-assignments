# Task: Use concatenation (+) and repetition (*) to create a pattern.
# Expected outcome:
# - banner should be exactly: '---GO!---'

left = "-" * __
center = "GO!" * __
right = "-" * __

banner = left + center + right
print(banner)
