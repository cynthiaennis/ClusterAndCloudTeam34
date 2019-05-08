import json

with open("user.txt", "w") as f:
    f.write(json.dumps({"seem_user": list(set([2, 3, 4, 4]))}))
