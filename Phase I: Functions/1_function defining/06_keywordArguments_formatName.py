# Define a function named format_name with parameters:
# - first
# - last
# - middle (default "")
# It returns:
# - If middle is empty: "<last>, <first>"
# - Otherwise: "<last>, <first> <middle>"
# Then call it using keyword arguments exactly as shown and print results.

# TODO: define format_name(first, last, middle="")

print(format_name(first="Ada", last="Lovelace"))
print(format_name(last="Turing", first="Alan", middle="Mathison"))

# Expected outcome (exact):
# Lovelace, Ada
# Turing, Alan Mathison
