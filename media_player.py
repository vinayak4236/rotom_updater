import subprocess, os, json
import urllib.parse
import webbrowser
from difflib import get_close_matches

# ---------- Spotify Web-API-free approach ----------
def _spotify_search_and_play(query: str) -> str:
    """
    Uses Spotify’s desktop protocol URL.
    Falls back to opening Spotify search if track not found.
    """
    encoded = urllib.parse.quote(query)
    uri = f"spotify:search:{encoded}"
    try:
        # Try to launch the URI (works if Spotify desktop is installed)
        os.startfile(uri)
        return f"Searching Spotify for '{query}'"
    except Exception as e:
        return f"Couldn’t open Spotify: {e}"

# ---------- YouTube ----------
def _youtube_search_and_play(query: str) -> str:
    encoded = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    return f"Opened YouTube search for '{query}'"

# ---------- VLC (local files) ----------
VLC_EXE = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
MUSIC_FOLDER = os.path.expanduser("~/Music")

def _vlc_play(query: str) -> str:
    """
    Very naive: walks ~/Music for any file whose name contains <query>.
    """
    if not os.path.isfile(VLC_EXE):
        return "VLC not found at default path."

    candidates = []
    for root, _, files in os.walk(MUSIC_FOLDER):
        for f in files:
            if f.lower().endswith((".mp3", ".flac", ".wav", ".m4a")):
                if query.lower() in f.lower():
                    candidates.append(os.path.join(root, f))

    if not candidates:
        return f"No local song matching '{query}' found in {MUSIC_FOLDER}."
import os, subprocess, urllib.parse, json
import webbrowser
import yt_dlp

# ---------- YOUTUBE ----------
def _play_youtube(query: str) -> str:
    ydl_opts = {"quiet": True, "skip_download": True, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if not info["entries"]:
            return f"No YouTube results for '{query}'."
        url = info["entries"][0]["webpage_url"]
        webbrowser.open(url + "&autoplay=1")   # most browsers honour autoplay
        title = info["entries"][0]["title"]
        return f"Playing '{title}' on YouTube."

# ---------- SPOTIFY ----------
def _play_spotify(query: str) -> str:
    """
    Uses Spotify URI scheme that the desktop client understands.
    It will auto-play the first hit if Spotify is installed & logged in.
    """
    encoded = urllib.parse.quote(query)
    uri = f"spotify:search:{encoded}"
    try:
        os.startfile(uri)
        return f"Playing '{query}' on Spotify."
    except Exception as e:
        return f"Couldn’t open Spotify: {e}"

# ---------- VLC LOCAL ----------
VLC_EXE = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
MUSIC_FOLDER = os.path.expanduser("~/Music")

def _play_vlc(query: str) -> str:
    if not os.path.isfile(VLC_EXE):
        return "VLC not found."

    matches = []
    for root, _, files in os.walk(MUSIC_FOLDER):
        for f in files:
            if f.lower().endswith((".mp3", ".flac", ".wav", ".m4a", ".mp4", ".mkv")):
                if query.lower() in f.lower():
                    matches.append(os.path.join(root, f))
    if not matches:
        return f"No local file matching '{query}' in {MUSIC_FOLDER}."

    best = min(matches, key=lambda p: len(os.path.basename(p)))
    subprocess.Popen([VLC_EXE, "--play-and-exit", best])
    return f"Playing {os.path.basename(best)} in VLC."
    # play the best match
    best = min(candidates, key=lambda p: len(os.path.basename(p)))  # shortest match
    subprocess.Popen([VLC_EXE, best])
    return f"Playing {os.path.basename(best)} in VLC."
