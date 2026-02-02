# Goal: Practice positional-only and keyword-only parameters.
# Expected outcome: Running the file prints exactly:
# 7
# 15

# TODO: Define clamp(x, /, *, low=0, high=10)
# - x must be positional-only
# - low and high must be keyword-only
# Return:
# - low if x < low
# - high if x > high
# - otherwise x

def clamp(x, /, *, low=0, high=10):
    

print(clamp(7, low=0, high=10))
print(clamp(20, low=0, high=15))
