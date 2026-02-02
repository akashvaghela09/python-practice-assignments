# Define a function named build_query that accepts keyword arguments using **kwargs.
# It returns a query string with keys sorted alphabetically.
# Format: key=value pairs joined by "&".
# Values must be converted to strings with str().
# Example: build_query(b=2, a=1) -> "a=1&b=2"
# Then print the results of the two calls below on separate lines.

# TODO: define build_query(**kwargs)

print(build_query(page=2, q="python"))
print(build_query(z=0, a=10, m=5))

# Expected outcome (exact):
# page=2&q=python
# a=10&m=5&z=0
