# Goal: Join parts into a URL path with '/' and print it.
# Expected output:
# api/v1/users

parts = ["api", "v1", "users"]

path = ("/".join(parts)) # TODO
print(path)
