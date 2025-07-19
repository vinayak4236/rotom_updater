import psutil, datetime
from modules.memory import recall
from modules.speech_output import speak

def _battery_summary() -> str:
    battery = psutil.sensors_battery()
    if battery is None:
        return "Plugged-in (no battery info)"
    percent = battery.percent
    plug = "charging" if battery.power_plugged else "on battery"
    return f"{int(percent)}% {plug}"

def _cpu_summary() -> str:
    load = psutil.cpu_percent(interval=1)  # 1-sec average
    return f"{int(load)}%"

def _greeting() -> str:
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

def _task_count() -> int:
    # For now, just count stored reminders.
    # Extend later with calendar, to-do list, etc.
    reminders = recall("reminders", [])
    return len(reminders)

def run_personal_mode():
    name = recall("name") or "there"
    greet = _greeting()
    cpu  = _cpu_summary()
    batt = _battery_summary()
    tasks = _task_count()

    line = (f"{greet}, {name}! "
            f"CPU at {cpu}, battery at {batt}. "
            f"You have {tasks} task{'s' if tasks!=1 else ''} today.")
    speak(line)