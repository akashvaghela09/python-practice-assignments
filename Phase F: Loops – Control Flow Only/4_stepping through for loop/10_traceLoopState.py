# Goal: Produce a trace log showing step-by-step loop state.
# Expected outcome (exact lines):
# i=0 before=1 after=1
# i=1 before=1 after=2
# i=2 before=2 after=6
# i=3 before=6 after=24
# final: 24

# Rule: On each iteration, multiply result by (i if i > 0 else 1)
# and print the trace line using the exact format above.

result = ____
for i in range(____):
    before = ____
    if i > 0:
        result = result * ____
    else:
        result = result * ____
    print("i=" + str(i) + " before=" + str(before) + " after=" + str(result))
print("final:", result)