# Goal: Read words until the word "STOP" is entered. If you find the target word first, break.
# Target word is "python".
# Expected outcome:
# - If inputs: java, ruby, python, STOP -> print exactly: Found target
# - If inputs: java, ruby, STOP -> print exactly: Not found

target = "python"
found = False

while True:
    word = input()
    # TODO: if word is "STOP", break
    # TODO: if word matches target, set found True and break
    pass

# TODO: print "Found target" if found else "Not found"
