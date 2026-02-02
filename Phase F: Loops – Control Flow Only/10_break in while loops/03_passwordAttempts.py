# Goal: Ask for a password up to 3 times. If correct, break early.
# Password is: "python"
# Expected outcome:
# - If the inputs are: java, ruby, python -> print exactly: Access granted
# - If the inputs are: java, ruby, go -> print exactly: Access denied

PASSWORD = "python"
attempts = 0

while attempts < 3:
    guess = input()
    # TODO: if guess matches PASSWORD, print "Access granted" and break
    # TODO: otherwise, increment attempts
    pass

# TODO: if loop ended because attempts reached 3 (and no break happened), print "Access denied"
