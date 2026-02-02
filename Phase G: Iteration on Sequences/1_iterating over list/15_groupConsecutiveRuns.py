# Group consecutive equal values into runs (a list of lists) and print it.
# Example: [1,1,2,2,2,3,1,1] -> [[1,1],[2,2,2],[3],[1,1]]
# Expected outcome:
# [[1, 1], [2, 2, 2], [3], [1, 1]]

nums = [1, 1, 2, 2, 2, 3, 1, 1]

runs = ____
current_run = ____

for n in ____:
    if current_run == [] or ____:
        current_run.append(____)
    else:
        runs.append(____)
        current_run = [____]

# TODO: after the loop, append the last run if needed
if ____:
    runs.append(____)

print(runs)
