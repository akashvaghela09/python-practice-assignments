# Goal: Keep reading integers until the user enters -1, then stop using break.
# Expected outcome: After inputs 3, 8, -1 the program prints exactly: You entered 2 numbers

count = 0

while True:
    n = int(input())
    # TODO: if n is -1, stop the loop using break
    # TODO: otherwise, increase count
    pass

print(f"You entered {count} numbers")
