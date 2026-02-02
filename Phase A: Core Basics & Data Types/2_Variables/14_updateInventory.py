# Goal: Track inventory with multiple variable updates.
# Start with stock=30.
# Then apply these events in order:
# - sold 7
# - received 12
# - sold 5
# Expected output (exactly 4 lines):
# start=30
# after_sold1=23
# after_received=35
# after_sold2=30

stock = 30
print("start=" + str(stock))

# TODO: update stock after selling 7; store in after_sold1
print("after_sold1=" + str(after_sold1))

# TODO: update stock after receiving 12; store in after_received
print("after_received=" + str(after_received))

# TODO: update stock after selling 5; store in after_sold2
print("after_sold2=" + str(after_sold2))
