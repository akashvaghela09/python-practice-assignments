# Goal: Allow up to 3 attempts to enter the correct password.
# If the correct password is entered, print 'Access granted'. Otherwise, after 3 failures, print 'Access denied'.
# Use a while loop.
# With inputs: a, b, secret
# Expected outcome (exact line):
# Access granted

correct = "secret"
attempts = 0

# TODO: loop while attempts remain and password not correct
entered = input("Password: ")
while __________:
    attempts = __________
    entered = input("Password: ")

# TODO: print the correct final message
if __________:
    print("Access granted")
else:
    print("Access denied")
