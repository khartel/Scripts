# install_usb_guard.py — run once as Administrator

import os
import subprocess

script_path = r"C:\Scripts\usb_guard.py"

# Find pythonw.exe (silent background python)
python_dir = os.path.dirname(subprocess.getoutput("where python").splitlines()[0])
pythonw_path = os.path.join(python_dir, "pythonw.exe")

# Fallback to python.exe if pythonw not found
if not os.path.exists(pythonw_path):
    pythonw_path = subprocess.getoutput("where python").splitlines()[0]

print(f"Using Python: {pythonw_path}")
print(f"Script path: {script_path}")

# Build the schtasks command properly
result = subprocess.run([
    "schtasks", "/create",
    "/tn", "USBGuard",
    "/tr", f'"{pythonw_path}" "{script_path}"',
    "/sc", "onlogon",
    "/rl", "highest",
    "/f"
], capture_output=True, text=True)

if result.returncode == 0:
    print("✓ USB Guard installed! It will start automatically at every login.")
else:
    print("✗ Installation failed:")
    print(result.stderr)