import pyttsx3
import threading
import time
import os

engine = pyttsx3.init()

# -------------------------------------------------
# Lazy-start avatar thread
# -------------------------------------------------
_avatar = None
_avatar_started = False

def _start_avatar():
    global _avatar
    try:
        from modules.avatar import SciFiAvatar
        _avatar = SciFiAvatar()
        _avatar.run()
    except Exception as e:
        # silently disable avatar if image missing / any error
        print("Avatar disabled:", e)

# -------------------------------------------------
# Public speak()
# -------------------------------------------------
def speak(text: str):
    global _avatar_started
    if not _avatar_started:
        threading.Thread(target=_start_avatar, daemon=True).start()
        _avatar_started = True
        time.sleep(0.4)          # give Tk time to show

    print("Rotom:", text)
    if _avatar is not None:
        _avatar.start_talking()
    engine.say(text)
    engine.runAndWait()
    if _avatar is not None:
        _avatar.stop_talking()