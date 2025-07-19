import json, os, time
MEM_FILE = "rotom_memory.json"

def _load():
    if not os.path.exists(MEM_FILE):
        return {"name": None, "prefs": {}, "last": None, "history": []}
    with open(MEM_FILE, encoding="utf-8") as f:
        return json.load(f)

def _save(mem):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

def remember(key, value):
    mem = _load()
    mem[key] = value
    _save(mem)

def recall(key, default=None):
    return _load().get(key, default)

def add_history(user_txt, bot_txt):
    mem = _load()
    mem["history"].append({"time": time.time(), "user": user_txt, "bot": bot_txt})
    mem["history"] = mem["history"][-10:]  # keep last 10
    _save(mem)