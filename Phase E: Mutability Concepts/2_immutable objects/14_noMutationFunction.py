# Goal: Write a function that accepts a tuple and returns a modified NEW tuple without mutating input.
# Expected outcome:
# - Prints: "in: (10, 20, 30)"
# - Prints: "out: (10, 99, 30)"
# - Prints: "same input object: True" (input variable still refers to original tuple)

def replace_at(t, index, value):
    """Return a new tuple equal to t but with t[index] replaced by value."""
    # TODO: implement using slicing and concatenation
    pass

inp = (10, 20, 30)
out = replace_at(inp, 1, 99)

print("in:", inp)
print("out:", out)
print("same input object:", inp is (10, 20, 30))
