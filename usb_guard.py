import win32api
import win32con
import win32security
import subprocess
import ctypes
import sys
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

# ─────────────────────────────────────────
#  SET YOUR PASSWORD HERE
PASSWORD = "testing123"
# ─────────────────────────────────────────


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def block_drive(drive_letter):
    """Deny all access to the drive using icacls."""
    path = f"{drive_letter}\\"
    subprocess.run(
        ["icacls", path, "/deny", "Everyone:(OI)(CI)F"],
        capture_output=True
    )
    print(f"[BLOCKED] {drive_letter}")


def unblock_drive(drive_letter):
    """Restore access to the drive."""
    path = f"{drive_letter}\\"
    subprocess.run(
        ["icacls", path, "/remove:d", "Everyone"],
        capture_output=True
    )
    print(f"[UNLOCKED] {drive_letter}")


def eject_drive(drive_letter):
    """Eject the drive."""
    shell = ctypes.windll.shell32
    drive_path = f"{drive_letter}\\"
    # Use Windows API to eject
    subprocess.run(
        ["powershell", "-Command",
         f"$shell = New-Object -ComObject Shell.Application; "
         f"$shell.Namespace(17).ParseName('{drive_letter}').InvokeVerb('Eject')"],
        capture_output=True
    )
    print(f"[EJECTED] {drive_letter}")


def prompt_password(drive_letter):
    """Show a GUI password prompt."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring to front

    entered = simpledialog.askstring(
        "USB Drive Detected",
        f"A USB drive was connected at {drive_letter}.\n\nEnter password to grant access:",
        show='*',
        parent=root
    )
    root.destroy()
    return entered


def handle_new_drive(drive_letter):
    """Called when a new USB drive is detected."""
    print(f"[DETECTED] New drive: {drive_letter}")

    # Step 1: Block immediately
    block_drive(drive_letter)

    # Step 2: Prompt for password
    entered_password = prompt_password(drive_letter)

    # Step 3: Check password
    if entered_password == PASSWORD:
        unblock_drive(drive_letter)
        messagebox.showinfo("USB Guard", f"✓ Access granted to {drive_letter}")
        print(f"[ACCESS GRANTED] {drive_letter}")
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("USB Guard", f"✗ Wrong password. Ejecting {drive_letter}...")
        root.destroy()
        eject_drive(drive_letter)
        print(f"[ACCESS DENIED] {drive_letter}")


def get_removable_drives():
    """Get current list of removable drive letters."""
    drives = []
    bitmask = win32api.GetLogicalDrives()
    for i in range(26):
        if bitmask & (1 << i):
            letter = f"{chr(65 + i)}:"
            try:
                drive_type = win32api.GetDriveType(f"{letter}\\")
                if drive_type == win32con.DRIVE_REMOVABLE:
                    drives.append(letter)
            except:
                pass
    return drives


def monitor():
    """Main loop — watches for new USB drives."""
    print("USB Guard is running. Waiting for drives...")
    known_drives = set(get_removable_drives())

    while True:
        time.sleep(1)
        current_drives = set(get_removable_drives())
        new_drives = current_drives - known_drives

        for drive in new_drives:
            handle_new_drive(drive)

        known_drives = current_drives


if __name__ == "__main__":
    if not is_admin():
        # Re-launch as admin if not already
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    else:
        monitor()