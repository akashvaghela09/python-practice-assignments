# Goal: Process multiple lines of input. Each line contains space-separated integers.
# Use a while loop to read lines until the line "END" is entered.
# For each line, scan numbers left-to-right and stop scanning that line when you hit 0 (break).
# Keep a grand total of all numbers processed (excluding zeros and excluding numbers after the first 0 in each line).
# Expected outcome:
# If the input lines are:
# "1 2 0 100"
# "5 5"
# "9 0 9"
# "END"
# Then the program prints exactly: Total: 22

grand_total = 0

while True:
    line = input().strip()
    # TODO: if line == "END", break out of the outer loop

    parts = line.split()
    i = 0
    while i < len(parts):
        num = int(parts[i])
        # TODO: if num == 0, break out of the inner loop
        # TODO: otherwise add num to grand_total
        i += 1

print(f"Total: {grand_total}")
