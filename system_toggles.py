import subprocess

def _run_powershell(script: str) -> str:
    """Run a PowerShell command and return the first line of stdout or error."""
    try:
        out = subprocess.check_output(
            ["powershell", "-Command", script],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=6
        ).strip()
        return out.splitlines()[0] if out else "Done"
    except subprocess.CalledProcessError as e:
        return e.stdout.strip() or "Command failed (admin rights may be needed)."

# ---------- Wi-Fi ----------
def wifi_on():
    return _run_powershell("netsh interface set interface name=Wi-Fi admin=enabled")

def wifi_off():
    return _run_powershell("netsh interface set interface name=Wi-Fi admin=disabled")

# ---------- Bluetooth ----------
def bluetooth_on():
    return _run_powershell("Start-Service -Name bthserv; Set-Service -Name bthserv -StartupType Automatic")

def bluetooth_off():
    return _run_powershell("Stop-Service -Name bthserv -Force")

# ---------- Airplane Mode ----------
def airplane_on():
    return _run_powershell("Set-ItemProperty -Path HKLM:\\SYSTEM\\CurrentControlSet\\Control\\RadioManagement\\SystemRadioState -Name Value -Value 1")

def airplane_off():
    return _run_powershell("Set-ItemProperty -Path HKLM:\\SYSTEM\\CurrentControlSet\\Control\\RadioManagement\\SystemRadioState -Name Value -Value 0")