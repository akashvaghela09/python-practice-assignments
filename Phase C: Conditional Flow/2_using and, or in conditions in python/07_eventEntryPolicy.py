# Goal: Determine if someone can enter an event.
# Rules:
# - Must have ticket.
# - If age < 18, must also be accompanied.
# - VIPs can enter without a ticket only if they are on the guest list.
# Print exactly: ENTER or DENY
# Expected outcome:
# With has_ticket=False, is_vip=True, on_guest_list=True, age=25, accompanied=False => ENTER
# With has_ticket=True, is_vip=False, on_guest_list=False, age=16, accompanied=False => DENY

has_ticket = False
is_vip = True
on_guest_list = True
age = 25
accompanied = False

# TODO: Build the condition using 'and'/'or' to match the policy.
# Hint: Break it into parts like regular_entry, vip_entry.
regular_entry = ____
vip_entry = ____

if ____:
    print("ENTER")
else:
    print("DENY")
