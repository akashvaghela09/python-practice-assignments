# You are generating seat labels for a 3x4 grid: rows A-C and columns 1-4.
# Skip any seat that appears in blocked using continue.
# Print each allowed seat on its own line, in row-major order.
# Expected outcome (exact lines):
# A1
# A2
# A4
# B1
# B2
# B3
# B4
# C1
# C3
# C4

rows = ["A", "B", "C"]
cols = [1, 2, 3, 4]
blocked = {"A3", "C2"}

for r in rows:
    for c in cols:
        seat = f"{r}{c}"
        # TODO: if seat is blocked, continue
        
        print(seat)
