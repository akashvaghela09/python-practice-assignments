# Parse multiple records separated by ';' where each record is key:value.
# Build a dictionary and print it.
# Expected outcome: prints {'name': 'Ada', 'lang': 'Python', 'year': '2026'}

text = "name:Ada;lang:Python;year:2026"
records = text.split(___)
result = {}
for rec in records:
    key, value = rec.split(___)
    # store into result
    ___
print(result)
