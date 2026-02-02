# Compute the average of only valid scores in the inclusive range 0..100.
# Use continue to skip invalid scores.
# Print the average as a float with exactly 2 decimal places.
# Expected outcome (exact):
# 76.67

scores = [90, 105, 70, -5, 80, 60, 200]

valid_sum = 0
valid_count = 0
for score in scores:
    # TODO: if score is outside 0..100, continue
    
    valid_sum += score
    valid_count += 1

avg = valid_sum / valid_count
print(f"{avg:.2f}")
