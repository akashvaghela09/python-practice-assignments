# Goal: Split the CSV line into fields and print them joined by ' | '.
# Expected output:
# Ada | Lovelace | 36

line = "Ada,Lovelace,36"

parts = line.split(",") # TODO: split into a list
print(" | ".join(parts))
