# Goal: Validate a login attempt.
# Rule: access granted if username is not empty AND (password matches OR has_reset_token)
# Expected outcome:
# With username='sam', password='secret', expected_password='secret', has_reset_token=False => ACCESS GRANTED
# With username='sam', password='wrong', expected_password='secret', has_reset_token=False => ACCESS DENIED

username = "sam"
password = "secret"
expected_password = "secret"
has_reset_token = False

# TODO: Use 'and'/'or' to implement the rule.
if ____:
    print("ACCESS GRANTED")
else:
    print("ACCESS DENIED")
