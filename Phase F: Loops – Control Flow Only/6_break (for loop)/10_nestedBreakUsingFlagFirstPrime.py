# Goal: Find the first prime number in the list and print it.
# Use a nested for-loop to test divisibility.
# Use break to stop checking divisors when a divisor is found.
# Use a flag variable to decide if the number is prime.
# Once the first prime is printed, stop the outer loop using break.
# Expected outcome:
# 29

nums = [1, 21, 25, 29, 35, 37]

for n in nums:
    # TODO: skip numbers less than 2
    is_prime = True

    # TODO: test divisors from 2 up to n-1 (or a smarter limit if you want)
    for d in range(2, n):
        # TODO: if n % d == 0, set is_prime to False and break
        pass

    # TODO: if is_prime is True, print n and break out of the outer loop
    pass
