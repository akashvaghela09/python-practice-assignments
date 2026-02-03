# Goal: Use an f-string (or format) to produce the exact message.
# Expected output:
# User Ada has 5 new messages.

name = "Ada"
new_messages = 5

message = (f"User {name} has {new_messages} new messages.")  # TODO
print(message)
