# Goal: Use 'in' / 'not in' in a more complex setting: seat availability in a 2D grid.
# Seats are labeled like 'A1', 'A2', ... rows A-C and columns 1-4.
# Some seats are reserved; determine which requested seats are available.
# Expected outcome:
# - Prints exactly:
#   available: ['A1', 'B4']
#   unavailable: ['A2', 'C3']

rows = ["A", "B", "C"]
cols = [1, 2, 3, 4]

reserved = {"A2", "C3", "B1"}
requested = ["A1", "A2", "B4", "C3"]

# TODO: Build a full set of valid seats (e.g., {'A1', ...}) using rows and cols
valid_seats = None

available = []
unavailable = []

for seat in requested:
    # TODO: A seat is available only if it is in valid_seats AND not in reserved
    if None:
        available.append(seat)
    else:
        unavailable.append(seat)

print(f"available: {available}")
print(f"unavailable: {unavailable}")
