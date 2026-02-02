# Goal: Keep reading input until the user types 'quit' (case-sensitive).
# Count how many non-quit lines were entered and print the count once finished.
# Example interaction:
# input: hello
# input: world
# input: quit
# Expected outcome (exact line):
# You entered 2 lines

count = 0

# TODO: use a while loop to repeatedly call input() until 'quit'
text = input("Enter text (or quit): ")
while __________:
    count = __________
    text = input("Enter text (or quit): ")

print("You entered", count, "lines")
