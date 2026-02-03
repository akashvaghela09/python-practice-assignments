# Goal: Write a function that validates types and returns specific strings.
# Expected outcome: Running this file prints exactly:
# ok:int
# ok:float
# error:expected number
# ok:bool
# error:expected number
#
# Rules for classify_number(value):
# - If value is an int (but NOT a bool), return "ok:int"
# - If value is a float, return "ok:float"
# - If value is a bool, return "ok:bool"
# - Otherwise return "error:expected number"

def classify_number(value):
    if isinstance(value,bool):
        return "ok:bool"
    elif isinstance(value,float):
        return "ok:float"
    elif isinstance(value,int):
        return "ok:int"
    else:
        return "error:expected number"
    
    # TODO: Implement using type checks.
    

print(classify_number(5))
print(classify_number(2.5))
print(classify_number("3"))
print(classify_number(True))
print(classify_number(None))
