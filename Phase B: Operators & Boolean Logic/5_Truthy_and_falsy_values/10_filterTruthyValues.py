# Task: Filter out falsy values while keeping truthy ones, preserving order.
# Falsy values in Python include: 0, 0.0, "", [], {}, set(), None, False
# Complete the function so that the program prints exactly:
# "[1, 'hi', [0], True, {'x': 1}]"

def keep_truthy(values):
    kept = []
    for v in values:
        if __:
            __
    return kept

data = [0, 1, "", "hi", [], [0], None, False, True, {}, {"x": 1}]
print(keep_truthy(data))
