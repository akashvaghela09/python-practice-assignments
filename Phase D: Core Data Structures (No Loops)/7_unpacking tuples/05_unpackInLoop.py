# Use tuple unpacking in a loop over a list of pairs and build a formatted string.

points = [(1, 2), (3, 4), (5, 6)]

result_lines = []
# TODO: loop through points, unpack each (x, y), and append "x=<x>, y=<y>" to result_lines

output = "\n".join(result_lines)
print(output)
# Expected outcome:
# x=1, y=2
# x=3, y=4
# x=5, y=6
