# Task: Implement validate_payload(payload) for an API-like request body.
# Payload rules:
# - payload must be a dict else TypeError("payload must be a dict")
# - Required keys: "action", "data"
#   If missing, raise KeyError("missing key: <key>")
# - No extra keys allowed besides "action", "data", "meta"
#   If extra, raise TypeError("unexpected key: <key>")
# - action must be one of: "create", "update", "delete" else ValueError("invalid action")
# - data must be a dict else TypeError("data must be a dict")
# - For action "create": data must include non-empty str "name" and numeric "price" > 0
# - For action "update": data must include int "id" > 0 and may include "name" and/or "price" (if present, must meet same constraints)
# - For action "delete": data must include int "id" > 0 and must not include any other keys
# - meta (optional) must be a dict if provided else TypeError("meta must be a dict")
# Invalid handling messages:
# - For missing/invalid fields in data, raise ValueError with one of:
#   "invalid name", "invalid price", "invalid id", "invalid data keys"
# Expected outcome:
# - validate_payload({"action":"create","data":{"name":"Pen","price":1.5}}) returns True
# - validate_payload({"action":"delete","data":{"id":2,"name":"x"}}) raises ValueError("invalid data keys")
# - validate_payload({"action":"update","data":{"id":0}}) raises ValueError("invalid id")


def validate_payload(payload):
    # TODO: validate payload and return True when valid
    pass


if __name__ == "__main__":
    print(validate_payload({"action": "create", "data": {"name": "Pen", "price": 1.5}}))