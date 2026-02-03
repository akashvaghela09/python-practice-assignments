# Goal: Round a float to 2 decimals and print exactly two decimal places.
# Expected outcome (exact lines):
# 3.14
# 3.14

x = 3.14159

rounded =  round(x,2)# use round
formatted = f"{x:.2f}"# use f-string formatting to 2 decimal places

print(rounded)
print(formatted)
