# Goal: Parse numbers in different bases from strings and sum them.
# Expected outcome (exact lines):
# 31
# 31
# 62

s1 = "0b11111"  # 31 in binary with prefix
s2 = "1F"       # 31 in hex without prefix

n1 = int(s1, 2) # parse s1 correctly
n2 = int(s2,16) # parse s2 correctly as hex

print(n1)
print(n2)
print(n1 + n2)
