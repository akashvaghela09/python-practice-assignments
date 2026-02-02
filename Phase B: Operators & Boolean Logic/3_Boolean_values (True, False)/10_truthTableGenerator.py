# Assignment 10: Generate a truth table for a boolean expression
# Goal: Print a 4-line truth table for: (A and not B) or (not A and B)
# This is XOR: True when exactly one of A or B is True.

# TODO: Complete the code to iterate over all combinations of A and B in this order:
# (False, False), (False, True), (True, False), (True, True)

pairs = [
    (False, False),
    (False, True),
    (True, False),
    (True, True)
]

for A, B in pairs:
    # TODO: Compute result for (A and not B) or (not A and B)
    result = 
    # TODO: Print exactly in this format:
    # A=<value> B=<value> => <result>
    print()

# Expected output (4 lines):
# A=False B=False => False
# A=False B=True => True
# A=True B=False => True
# A=True B=True => False
