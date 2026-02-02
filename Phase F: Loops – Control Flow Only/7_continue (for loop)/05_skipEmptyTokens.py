# Split the string by commas, then print only non-empty trimmed tokens, one per line.
# Use continue to skip tokens that become empty after stripping.
# Expected outcome (exact lines):
# apple
# banana
# pear

raw = " apple, ,banana,  , pear,"
parts = raw.split(",")

for token in parts:
    cleaned = token.strip()
    # TODO: if cleaned is empty, continue
    
    print(cleaned)
