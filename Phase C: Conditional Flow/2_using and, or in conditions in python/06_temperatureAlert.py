# Goal: Print an alert category based on temperature and humidity.
# Rules:
# - Print DANGER if temperature >= 40 OR (temperature >= 35 AND humidity >= 70)
# - Else print OK
# Expected outcome:
# With temperature=36, humidity=75 => print exactly: DANGER
# With temperature=34, humidity=80 => print exactly: OK

temperature = 36
humidity = 75

# TODO: Use 'and'/'or' with correct precedence (use parentheses where needed).
if ____:
    print("DANGER")
else:
    print("OK")
