# Split only on the first colon and keep the rest intact.
# Expected outcome: prints header | a:b:c

s = "header:a:b:c"
left, right = s.split(___, ___)
print(left, "|", right)
