# starter.py  (never deleted)
import os, subprocess, sys, urllib.request, json, tempfile, zipfile, shutil

MANIFEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/rotom-updater/main/manifest.json"

def fetch(url):
    return urllib.request.urlopen(url).read()

def start():
    manifest = json.loads(fetch(MANIFEST_URL).decode())
    version = manifest["version"]
    print(f"[starter] fetching version {version}")

    # download missing files
    for path, url in manifest["files"].items():
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if not os.path.exists(path):
            print("[starter] downloading", path)
            open(path, "wb").write(fetch(url))

    # hand off to main.py
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    start()