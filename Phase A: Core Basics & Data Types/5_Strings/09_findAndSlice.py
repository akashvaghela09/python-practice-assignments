# Goal: Extract and print the domain part from the email.
# Expected output:
# example.com

email = "user@example.com"

at_index = -1  # TODO: find the index of '@'
domain = email[5:]    # TODO: slice after '@'
print(domain)
