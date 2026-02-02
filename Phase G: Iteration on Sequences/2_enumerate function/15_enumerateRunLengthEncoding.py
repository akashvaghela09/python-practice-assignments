# Goal: Implement run-length encoding (RLE) for a string using enumerate.
# For consecutive repeated characters, output "<char><count>".
# Expected outcome:
# a3b1c4a2

s = "aaabccccaa"
parts = []

# TODO:
# Use enumerate to detect when a run ends.
# Build parts like ["a3", "b1", ...] and then print the joined string.
run_char = None
run_start = 0

for i, ch in enumerate(s):
    if run_char is None:
        run_char = ch
        run_start = i
        continue

    # TODO: If ch differs from run_char, close the previous run and start a new one.
    if ___:
        run_len = i - run_start
        parts.append(f"{run_char}{run_len}")
        run_char = ch
        run_start = i

# TODO: Close the final run after the loop.
___

print("".join(parts))
