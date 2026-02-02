# Goal: Parse a simple query string into a dictionary.
# Rules:
# - Pairs are separated by '&'
# - Key and value are separated by '='
# - Values should remain strings
# Expected outcome when run:
# {'lang': 'py', 'level': '2', 'mode': 'practice'}

query = "lang=py&level=2&mode=practice"
params = {}

# TODO: split query into pairs and fill params

print(params)
