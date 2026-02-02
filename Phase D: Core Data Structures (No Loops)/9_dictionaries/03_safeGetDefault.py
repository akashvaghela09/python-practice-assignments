# Goal: Use dict.get to avoid KeyError and provide a default.
# Expected outcome when run:
# guest
# 0

user = {
    "role": "guest"
}

print(user.get("role"))
# TODO: print user.get("logins", 0)
