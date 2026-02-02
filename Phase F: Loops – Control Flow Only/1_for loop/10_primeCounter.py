# Count how many prime numbers are in the list using for loops.
# A prime is an integer > 1 with no divisors other than 1 and itself.
# Expected outcome: print 5

nums = [2, 3, 4, 5, 9, 11, 12, 13]
prime_count = 0

# TODO: For each number, determine if it's prime using a nested for loop.
# Hints:
# - Assume is_prime = True for n > 1
# - Try divisors from 2 to n-1 (or to int(sqrt(n)) + 1 if you prefer)
# - If divisible, set is_prime = False and break
for n in ____:
    if n <= 1:
        continue
    is_prime = True
    for d in ____:
        if ____:
            is_prime = ____
            ____
    if ____:
        prime_count = ____

print(prime_count)
