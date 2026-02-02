# Goal: Implement a menu loop that runs until the user chooses to quit.
# Use break to exit when the user enters "q".
# Valid commands:
# - "inc": increment a counter
# - "dec": decrement a counter
# - "q": quit
# Any other input should be ignored.
# Expected outcome: For inputs inc, inc, dec, q the program prints exactly: Counter: 1

counter = 0

while True:
    cmd = input().strip()
    # TODO: if cmd is "q", break
    # TODO: if cmd is "inc", update counter
    # TODO: if cmd is "dec", update counter
    pass

print(f"Counter: {counter}")
