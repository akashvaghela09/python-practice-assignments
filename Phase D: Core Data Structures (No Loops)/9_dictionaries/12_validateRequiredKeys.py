# Goal: Validate required keys exist in each record.
# Expected outcome when run:
# 2

records = [
    {"id": 1, "name": "Kai"},
    {"id": 2},
    {"name": "Mina"},
    {"id": 4, "name": "Sol"}
]
required = {"id", "name"}
valid_count = 0

for rec in records:
    # TODO: if all required keys are present in rec, increment valid_count
    pass

print(valid_count)
