# Goal: Observe mutability differences between list and tuple using id().
# Expected outcome: Running this file prints two lines:
# Line 1: True
# Line 2: False
# (Meaning: the list keeps the same id after mutation; the tuple gets a new id after "modification".)

nums_list = [1, 2, 3]
nums_tuple = (1, 2, 3)

list_id_before = id(nums_list)
# TODO: Mutate the list in-place so it becomes [1, 2, 3, 4].

list_id_after = id(nums_list)

# For tuple, you cannot mutate in-place; you must create a new tuple.
tuple_id_before = id(nums_tuple)
# TODO: Create a new tuple assigned back to nums_tuple so it becomes (1, 2, 3, 4).

tuple_id_after = id(nums_tuple)

print(list_id_before == list_id_after)
print(tuple_id_before == tuple_id_after)
