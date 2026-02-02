# Goal: Process rows while skipping header; enumerate should reflect data row index starting at 1.
# Expected outcome:
# 1: Alice
# 2: Bob

rows = [
    "name,age",
    "Alice,30",
    "Bob,25"
]

# TODO:
# - Skip the header row
# - Use enumerate(..., start=1) over the remaining rows
# - Print "<n>: <name>" for each data row
for ___, ___ in ___:
    name = ___.split(",")[0]
    print(___)
