# Goal: Use a conditional (ternary) expression to select which dictionary key to read.
# If use_primary is True, pick "primary" else pick "backup".
# Expected outcome: Prints exactly: token=BK-999

config = {
    "primary": "PR-123",
    "backup": "BK-999"
}

use_primary = False

key = ________________________________

token = config[key]

print(f"token={token}")
