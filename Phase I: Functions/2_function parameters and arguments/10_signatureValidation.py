# Goal: Combine parameter types and validate inputs.
# Expected outcome: Running the file prints exactly:
# user=ana; role=admin; active=True
# user=bob; role=member; active=False

# TODO: Define format_user(user, /, role="member", *, active=True, **extra)
# Rules:
# - user is positional-only
# - role can be positional-or-keyword
# - active is keyword-only
# - extra keyword arguments must be ignored (but accepted)
# Return exactly: "user=<user>; role=<role>; active=<active>"

def format_user(user, /, role="member", *, active=True, **extra):
    

print(format_user("ana", "admin", active=True, theme="dark"))
print(format_user("bob", active=False))
