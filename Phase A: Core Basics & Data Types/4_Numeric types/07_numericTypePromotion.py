# Goal: Demonstrate type promotion in arithmetic and print resulting types.
# Expected outcome (exact lines):
# <class 'float'>
# <class 'complex'>

result1 = 5 + 2.0
result2 = 5 + 2j

print(type(result1))
print(type(result2))
