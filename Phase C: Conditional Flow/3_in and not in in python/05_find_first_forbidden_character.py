# Goal: Find the first character that is NOT allowed.
# Expected outcome:
# - Prints exactly:
#   forbidden: '#'

allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
text = "Meet me at 5#pm"

# TODO: Scan text from left to right and print the first forbidden character.
# If none are forbidden, print "forbidden: None"
for ch in text:
    if None:
        print(f"forbidden: {repr(ch)}")
        break
else:
    print("forbidden: None")
