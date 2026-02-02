# Goal: Sort version strings correctly (e.g., '1.10' > '1.2').
# Expected outcome: versions_sorted must be ['1.2', '1.9', '1.10', '2.0'].
# Constraint: Implement comparison via a comparator function and cmp_to_key.

from functools import cmp_to_key

versions = ['1.9', '1.10', '1.2', '2.0']

def compare_versions(a, b):
    # TODO: return -1 if a<b, 0 if a==b, 1 if a>b using numeric comparison of dot parts
    pass

# TODO: create versions_sorted using sorted() + cmp_to_key(compare_versions)

print(versions_sorted)
