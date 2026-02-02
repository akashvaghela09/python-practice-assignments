# Goal: Determine if a number n is prime using a while loop.
# Use break as soon as you find a divisor.
# Expected outcome:
# - Input: 29 -> print exactly: Prime
# - Input: 30 -> print exactly: Not prime

n = int(input())

if n < 2:
    print("Not prime")
else:
    d = 2
    is_prime = True
    while d * d <= n:
        # TODO: if n % d == 0, set is_prime False and break
        d += 1

    # TODO: print "Prime" if is_prime else "Not prime"
