# Print all prime numbers from 2 to 30 inclusive.
# Use a for loop over candidates, and an inner loop to test divisibility.
# Use continue in the outer loop to skip non-prime candidates.
# Expected outcome (exact):
# 2 3 5 7 11 13 17 19 23 29

primes = []

for n in range(2, 31):
    is_prime = True
    for d in range(2, n):
        # TODO: if n is divisible by d, set is_prime False and stop checking
        
        pass

    # TODO: if not prime, continue
    
    primes.append(n)

print(" ".join(str(p) for p in primes))
