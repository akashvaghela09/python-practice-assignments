# Task: Implement custom truthiness.
# Complete __bool__ so that:
# - A Cart is truthy when it has at least 1 item.
# - A Cart is falsy when it has 0 items.
# Expected output (2 lines) must be exactly:
# "EMPTY"
# "NOT EMPTY"

class Cart:
    def __init__(self, items):
        self.items = items

    def __bool__(self):
        __

c1 = Cart([])
c2 = Cart(["apple"])

print("NOT EMPTY" if c1 else "EMPTY")
print("NOT EMPTY" if c2 else "EMPTY")
