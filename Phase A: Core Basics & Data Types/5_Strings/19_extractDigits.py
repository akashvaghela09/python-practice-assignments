# Goal: Extract only digits from the text and print them as one string.
# Expected output:
# 15551234

text = "Call me at (1555) 1234!"

digits = ""
for charachter in text:
    if charachter.isdigit():
        digits += charachter# TODO: build a string containing only 0-9 characters
print(digits)
