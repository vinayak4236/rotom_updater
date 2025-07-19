import os
import webbrowser
import wikipedia
import requests
import datetime as dt
from modules.memory import remember, recall, add_history, _load, _save
from modules.messaging import fetch_unread_count, read_latest_unread, send_email, send_whatsapp
from modules.messaging import send_email

def clean_possessives(text: str) -> str:
    """Remove common possessive words to keep replies neat."""
    return text.replace("my ", "").replace("the ", "").replace("a ", "").strip()


def execute_command(command: str) -> str | None:
    print(f"[DEBUG] Received command: {command}")
    command = command.lower()

    # ---------- System Commands ----------
    if "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad..."

    elif "open calculator" in command:
        os.system("calc")
        return "Opening Calculator..."

    elif "open file explorer" in command or "open explorer" in command:
        os.system("explorer")
        return "Opening File Explorer..."

    elif "open whatsapp" in command:
        try:
            os.startfile("shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
            return "Opening WhatsApp..."
        except Exception:
            return "WhatsApp not found."

    elif "lock screen" in command or ("lock" in command and "screen" in command):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking the screen..."

    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down..."

    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting..."

    elif "log off" in command or "logout" in command:
        os.system("shutdown -l")
        return "Logging off..."

    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting the system to sleep..."

    # ---------- Small Talk & Memory ----------
    elif "hello" in command:
        return "Hi there!"

    elif "how are you" in command:
        return "I'm functioning perfectly. How can I help?"

    elif "thank you" in command or "thanks" in command:
        return "You're welcome!"

    elif "who are you" in command or "what are you" in command:
        return "I’m Rotom, your pocket AI assistant. I open apps, search the web, manage your PC, and remember stuff for you."

    elif "features" in command or "what can you do" in command:
        return "I can open programs, lock / sleep / shutdown / restart the computer, search anything online, and remember your preferences."

    elif "my name is" in command:
        name = command.replace("my name is", "").strip()
        remember("name", name)
        return f"Nice to meet you, {name}!"

    elif "what is my name" in command or "who am i" in command:
        n = recall("name")
        return f"Your name is {n}." if n else "I don’t know your name yet."

    elif "remember that" in command:
        fact = command.replace("remember that", "").strip()
        remember("last", fact)
        return "Got it, stored in memory."

    elif "what did i ask last" in command:
        last = recall("last")
        return f"You last asked: {last}" if last else "Nothing stored yet."

    elif "clear memory" in command:
        if os.path.exists("rotom_memory.json"):
            os.remove("rotom_memory.json")
        return "Memory cleared."

    elif command.startswith("what do i like"):
        likes = recall("likes")
        return f"You like {likes}." if likes else "I haven’t stored any likes yet."

    elif command.startswith("i like"):
        thing = clean_possessives(command[6:].strip())
        remember("likes", thing)
        return f"Noted! You like {thing}."

    elif any(k in command for k in ("recent chats", "history", "what did we talk about")):
        history = recall("history", [])
        if not history:
            return "No recent chats stored."
        lines = [f"{i+1}. You: {h['user'][:40]}…" for i, h in enumerate(history[-5:])]
        return "Last 5 things we discussed:\n" + "\n".join(lines)

    elif "clear history" in command:
        mem = _load()
        mem["history"] = []
        _save(mem)
        return "Chat history cleared."

    # ---------- Web Search ----------
    elif any(k in command for k in ("who is", "tell me about", "search for")):
        query = (
            command.replace("who is", "")
                   .replace("tell me about", "")
                   .replace("search for", "")
        ).strip()

        webbrowser.open(f"https://www.bing.com/search?q={query}")

        try:
            summary = wikipedia.summary(query, sentences=2)
            return f"Here’s what I found: {summary}"
        except Exception:
            return f"I opened a search for {query}, but I couldn’t grab a quick summary."

    elif command.startswith("remind me to"):
        msg = command.replace("remind me to", "").strip()
        # simple “in X minutes”
        if "in" in msg:
            try:
                rest, mins = msg.rsplit("in", 1)
                mins = int(mins.replace("minutes", "").replace("minute", "").strip())
                return schedule_reminder(rest.strip(), mins)
            except ValueError:
                pass
        return "Please say: remind me to <task> in <minutes>."

    elif command.startswith("open in"):
        try:
            _, rest = command.split("open in", 1)
            mins_str, app = rest.split("minutes", 1)
            mins = int(mins_str.strip())
            app = app.strip()
            # map friendly names → paths
            path_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "explorer": "explorer.exe"
            }
            app_path = path_map.get(app, app)
            return schedule_app(app_path, mins)
        except Exception:
            return "Usage: open in <minutes> <app-name>"
  
    # ---------- Messaging ----------
    elif "check unread emails" in command or "unread mails" in command:
        cnt = fetch_unread_count()
        return f"You have {cnt} unread email(s)."

    elif "read latest email" in command or "read my last email" in command:
        return read_latest_unread()

    elif command.startswith("send email to"):
        try:
            rest = command.replace("send email to", "").strip()
            to, rest = rest.split(" subject ", 1)
            if " body " in rest:
                subject, body = rest.split(" body ", 1)
            else:
                subject, body = rest, ""
            return send_email(to.strip(), subject.strip(), body.strip())
        except Exception:
            return "Usage: send email to <email> subject <subject> [body <message>]"

    elif command.startswith("send whatsapp to"):
        try:
            rest = command.replace("send whatsapp to", "").strip()
            phone, message = rest.split(" ", 1)
            return send_whatsapp(phone.strip(), message.strip())
        except:
            return "Usage: send whatsapp to <+phone> <message>"
    
    elif command.startswith("open "):
        app = command[5:].strip()
        if not app:
            return "Tell me what to open: 'open chrome', 'open spotify'…"
        from modules.app_launcher import launch
        return launch(app)
    
    elif command == "refresh app cache":
        from modules.app_launcher import _scan_system
        _scan_system()
        return "App list refreshed."

    # ---------- Media ----------
        # ---------- Media ----------
    elif command.startswith("play "):
        tail = command[5:].strip()
        if not tail:
            return "Tell me what to play, e.g. 'play Blinding Lights on Spotify'."

        if " on spotify" in tail:
            song = tail.replace(" on spotify", "").strip()
            from modules.media_player import _play_spotify
            return _play_spotify(song)

        elif " on youtube" in tail or " on yt" in tail:
            song = tail.replace(" on youtube", "").replace(" on yt", "").strip()
            from modules.media_player import _play_youtube
            return _play_youtube(song)

        elif " in vlc" in tail:
            song = tail.replace(" in vlc", "").strip()
            from modules.media_player import _play_vlc
            return _play_vlc(song)

        else:   # default → YouTube
            from modules.media_player import _play_youtube
            return _play_youtube(tail)

    # ---------- System Toggles ----------
    elif "turn on wifi" in command or "enable wifi" in command:
        from modules.system_toggles import wifi_on
        return wifi_on()

    elif "turn off wifi" in command or "disable wifi" in command:
        from modules.system_toggles import wifi_off
        return wifi_off()

    elif "turn on bluetooth" in command or "enable bluetooth" in command:
        from modules.system_toggles import bluetooth_on
        return bluetooth_on()

    elif "turn off bluetooth" in command or "disable bluetooth" in command:
        from modules.system_toggles import bluetooth_off
        return bluetooth_off()

    elif "turn on airplane mode" in command:
        from modules.system_toggles import airplane_on
        return airplane_on()

    elif "turn off airplane mode" in command:
        from modules.system_toggles import airplane_off
        return airplane_off()

    # ---------- Local Brain ----------
    elif command.endswith("?") or any(command.startswith(k) for k in (
            "what is", "who is", "tell me", "explain", "how to", "why")):
        from modules.brain import ask_brain
        return ask_brain(command)

    # ---------- Local Brain ----------
    elif any(command.startswith(k) for k in ("what is", "who is", "tell me", "explain", "how to", "capital of")) \
         or command.endswith("?"):
        from modules.brain import ask_brain
        return ask_brain(command)
    
    return None