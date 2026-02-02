# Goal: Aggregate a nested list of daily sales into per-store totals
# Expected outcome: running this file prints exactly: [('A', 19), ('B', 22), ('C', 0)]

# Each entry is (store_id, [list_of_daily_sales]).
# Some stores may have an empty list.
stores = [
    ("A", [5, 7, 7]),
    ("B", [10, 12]),
    ("C", [])
]

# TODO: build report as a list of (store_id, total_sales) in the same order as stores
report = None

print(report)
