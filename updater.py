# updater.py
import os, zipfile, requests, shutil, subprocess, sys, time

DRIVE_ID       = "1x2y3z4a5b6c7d8e9f0"      # <-- replace with your Drive file ID
VERSION_URL    = f"https://drive.google.com/uc?id={DRIVE_ID}&export=download"
PATCH_URL      = f"https://drive.google.com/uc?id={DRIVE_ID}&export=download"  # same zip file
PATCH_ZIP      = "patch.zip"
BACKUP_FOLDER  = "_backup"

def read_local_version():
    try:
        with open("version.txt") as f:
            return int(f.read().strip())
    except:
        return 0

def write_local_version(v):
    with open("version.txt", "w") as f:
        f.write(str(v))

def get_remote_version():
    try:
        txt = requests.get(VERSION_URL, timeout=5).text.strip()
        return int(txt)
    except:
        return read_local_version()

def download(url, file_name):
    r = requests.get(url, stream=True, timeout=15)
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def apply_patch():
    if not os.path.exists(PATCH_ZIP):
        return
    if os.path.exists(BACKUP_FOLDER):
        shutil.rmtree(BACKUP_FOLDER)
    shutil.copytree(".", BACKUP_FOLDER, dirs_exist_ok=True)
    with zipfile.ZipFile(PATCH_ZIP, 'r') as z:
        z.extractall(".")
    os.remove(PATCH_ZIP)

def restart():
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()

def check_and_update():
    local  = read_local_version()
    remote = get_remote_version()
    if remote > local:
        print("🔄 New update found. Downloading patch...")
        download(PATCH_URL, PATCH_ZIP)
        apply_patch()
        write_local_version(remote)
        print("✅ Update applied. Restarting...")
        time.sleep(1)
        restart()
    else:
        print("✅ Already up-to-date.")