import json

ids = [12345, 23456, 34567, 45678, 56789]
pl_list = {k: {"turn": False, "blown": False} for k in ids}

def next_user():
    next = False
    for v in pl_list.values():
        if next and not v["blown"]:
            v["turn"] = True
            return
        if v["turn"]:
            v["turn"], next = False, True
    for v in pl_list.values():
        if not v["blown"]:
            v["turn"] = True
            return

def turn_player():
    for v in pl_list.values():
        if v["turn"]: return v
    raise KeyError
    
while True:
    if input(json.dumps(pl_list, indent=4)) == "_":
        try: turn_player()["blown"] = True
        except KeyError: print("no players turn")
    next_user()
    