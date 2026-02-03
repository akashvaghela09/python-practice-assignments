# Goal: Print True if the filename ends with '.py' AND starts with 'test_'; otherwise print False.
# Expected output:
# True

filename = "test_strings.py"

is_valid = filename.startswith("test_")and filename.endswith(".py")  # TODO
print(is_valid)
