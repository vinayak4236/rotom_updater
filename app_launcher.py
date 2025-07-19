import os, subprocess, json
from difflib import get_close_matches

# One-time cache file so we don’t re-scan the disk on every query.
CACHE_FILE = "app_cache.json"

def _scan_system():
    """
    Build a dictionary  {friendly_name: full_path}  for
    - Start-menu shortcuts (.lnk)
    - Installed Microsoft Store apps (Appx)
    - Anything on %PATH%
    """
    cache = {}
    # 1) Start-menu shortcuts
    start_dirs = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
    ]
    for root in start_dirs:
        for dirpath, _, files in os.walk(root):
            for f in files:
                if f.lower().endswith(".lnk"):
                    name = os.path.splitext(f)[0].lower()
                    cache[name] = os.path.join(dirpath, f)

    # 2) Apps registered in registry (UWP + classic)
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths") as key:
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey) as sk:
                        path, _ = winreg.QueryValueEx(sk, "")
                        cache[subkey.lower().replace(".exe", "")] = path
                except OSError:
                    break
                i += 1
    except Exception:
        pass  # non-Windows systems

    # 3) Anything already on PATH
    for folder in os.environ["PATH"].split(";"):
        try:
            for item in os.listdir(folder):
                if item.lower().endswith(".exe"):
                    name = os.path.splitext(item)[0].lower()
                    cache[name] = os.path.join(folder, item)
        except (FileNotFoundError, PermissionError):
            pass

    with open(CACHE_FILE, "w") as fp:
        json.dump(cache, fp, indent=2)
    return cache

def _get_cache():
    if not os.path.exists(CACHE_FILE):
        return _scan_system()
    with open(CACHE_FILE) as fp:
        return json.load(fp)

def launch(app_name: str) -> str:
    """Return a message; raise on failure."""
    cache = _get_cache()
    name_key = app_name.lower().strip()

    if name_key in cache:
        path = cache[name_key]
    else:
        # fuzzy match
        matches = get_close_matches(name_key, cache.keys(), n=1, cutoff=0.6)
        if not matches:
            return f"Sorry, I couldn’t find an app called '{app_name}'."
        path = cache[matches[0]]

    try:
        os.startfile(path)
        return f"Opening {os.path.basename(path).replace('.lnk', '')}..."
    except Exception as e:
        return f"Couldn’t open {app_name}: {e}"