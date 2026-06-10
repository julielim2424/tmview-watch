import json

with open("seen.json", "w") as f:
    json.dump(["TEST123"], f)

print("UPDATED")
