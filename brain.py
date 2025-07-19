import os, json, difflib, webbrowser, wikipedia
from pathlib import Path
from modules.memory import recall, add_history

BRAIN_DIR = Path(__file__).parent.parent / "brain"
WEB_FALLBACK = True   # set False to disable web fallback

def _load_brain():
    """Return dict {slug: line} for fuzzy lookup."""
    kb = {}
    for txt in BRAIN_DIR.glob("*.txt"):
        for line in txt.read_text(encoding="utf-8").splitlines():
            if "|" in line:
                q, a = line.split("|", 1)
                kb[q.strip().lower()] = a.strip()
    return kb

_brain = _load_brain()

def ask_brain(query: str) -> str:
    query = query.lower().strip()

    # 1) exact / fuzzy match
    if query in _brain:
        ans = _brain[query]
        add_history(query, ans)
        return ans
    best = difflib.get_close_matches(query, _brain.keys(), n=1, cutoff=0.6)
    if best:
        ans = _brain[best[0]]
        add_history(query, ans)
        return ans

    # 2) web fallback
    if WEB_FALLBACK:
        try:
            summary = wikipedia.summary(query, sentences=2)
            add_history(query, summary)
            webbrowser.open(f"https://www.bing.com/search?q={query}")
            return f"Here’s what I found: {summary}"
        except Exception:
            webbrowser.open(f"https://www.bing.com/search?q={query}")
            return "I opened a search for you."
    return "I don’t know that yet."

def think():
    print("🧠 Brain module loaded. Ready for commands.")