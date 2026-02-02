# Goal: Print a login status message based on multiple conditions.
# Rules (in this order):
# - If username is empty -> "Missing username"
# - Elif password is empty -> "Missing password"
# - Elif locked is True -> "Account locked"
# - Elif username == correct_user AND password == correct_pass -> "Access granted"
# - Else -> "Access denied"
# Expected outcome for username="", password="abc", locked=False: Missing username

correct_user = "admin"
correct_pass = "s3cr3t"

username = ""
password = "abc"
locked = False

# TODO: Use if/elif/else to print exactly one status message

