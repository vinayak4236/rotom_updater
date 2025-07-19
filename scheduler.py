import os, time, threading, schedule
from datetime import datetime, timedelta
from modules.memory import remember, recall

ALARM_FILE = "rotom_reminders.json"

def _load_reminders():
    import json
    return recall("reminders", [])

def _save_reminders(lst):
    remember("reminders", lst)

def _run_reminder(text):
    from modules.speech_output import speak
    speak(f"Reminder: {text}")

def _run_app(path):
    os.startfile(path)

def schedule_reminder(text, delay_minutes):
    """delay_minutes = minutes from now"""
    def job():
        _run_reminder(text)
        # remove from list
        lst = _load_reminders()
        lst[:] = [r for r in lst if r["text"] != text]
        _save_reminders(lst)
    threading.Timer(delay_minutes * 60, job).start()

    lst = _load_reminders()
    lst.append({"text": text, "time": datetime.now().isoformat()})
    _save_reminders(lst)
    return f"Reminder set for {delay_minutes} minute(s)."

def schedule_app(app_path, delay_minutes):
    threading.Timer(delay_minutes * 60, lambda: _run_app(app_path)).start()
    return f"{os.path.basename(app_path)} will open in {delay_minutes} minute(s)."

def _cleanup_temp():
    temp_dir = os.getenv("TEMP")
    count = 0
    for f in os.listdir(temp_dir):
        try:
            full = os.path.join(temp_dir, f)
            if os.path.isfile(full):
                os.remove(full)
                count += 1
        except:
            pass
    from modules.speech_output import speak
    speak(f"Cleaned {count} temp files.")

def init_periodic_cleanup():
    # every Friday at 10:00
    schedule.every().friday.at("10:00").do(_cleanup_temp)
    def bg():
        while True:
            schedule.run_pending()
            time.sleep(60)
    threading.Thread(target=bg, daemon=True).start()