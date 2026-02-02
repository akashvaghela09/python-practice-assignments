# Assignment 9: Validate that all values in a list are booleans
# Goal: Complete the function so it returns True only if every element is exactly a bool.

def all_bools(values):
    # TODO: Iterate through values and verify each item is a bool.
    # Hint: Use type(x) is bool (not isinstance) to avoid counting ints.
    for v in values:
        
    return 

# Expected output (three lines):
# True
# False
# False
print(all_bools([True, False, True]))
print(all_bools([True, 1, False]))
print(all_bools([]))
