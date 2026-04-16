# 🔐 USB Guard

A lightweight Python tool for Windows that blocks access to any USB drive the moment it's plugged in — until the correct password is entered. Designed for anyone who wants to control exactly what gets accessed on their machine.

---

## 🚨 The Problem

By default, Windows automatically mounts any USB drive the moment it's plugged in — giving anyone instant access to your machine's files just by connecting a drive. USB Guard fixes that.

---

## ✅ How It Works

1. **USB drive is plugged in** → access is immediately blocked
2. A **password prompt** appears on screen
3. **Correct password** → drive is unlocked and accessible ✅
4. **Wrong password or cancelled** → drive is automatically ejected 🚫

---

## 🖥️ Requirements

- Windows 10 or 11 (Home, Pro, or Enterprise)
- Python 3.x
- Admin privileges (required for drive permission control)

### Python Dependencies

```bash
pip install pywin32
```

> `tkinter` is included with Python by default — no extra install needed.

---

## 📁 Files

| File | Description |
|------|-------------|
| `usb_guard.py` | The main guard script — monitors for USB drives and handles blocking/unlocking |
| `install_usb_guard.py` | One-time installer — registers the guard to auto-start at Windows login |

---

## ⚙️ Setup

### Step 1 — Set your password

Open `usb_guard.py` and change the password on this line:

```python
PASSWORD = "YourPasswordHere"
```

### Step 2 — Place the script somewhere permanent

Move `usb_guard.py` to a stable location, for example:

```
C:\Scripts\usb_guard.py
```

> ⚠️ Don't move or delete this file after installing — the scheduler points to this exact path.

### Step 3 — Run the installer (once)

Open PowerShell **as Administrator** and run:

```powershell
python C:\Scripts\install_usb_guard.py
```

You should see:

```
✓ USB Guard installed! It will start automatically at every login.
```

That's it. USB Guard will now run silently in the background every time you log into Windows.

---

## 🔄 How to Uninstall

To remove the auto-start task, open PowerShell as Administrator and run:

```powershell
schtasks /delete /tn "USBGuard" /f
```

---

## 🛡️ Security Notes

- The password is stored in plain text inside `usb_guard.py` — keep the file in a protected location and avoid sharing it
- This tool uses Windows `icacls` permission control to block drive access, which is effective against regular users
- A technically advanced user booting from a separate OS could bypass this — for stronger protection, consider combining with **BitLocker To Go**
- This tool is intended for personal use to prevent casual unauthorized access

---

## 💡 Planned Features

- [ ] System tray icon with status indicator
- [ ] Access attempt logging (timestamp + drive info)
- [ ] Lockout after N failed attempts
- [ ] Hashed password storage instead of plain text
- [ ] GUI settings panel

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> Built for Windows by someone who just wanted to keep their machine safe. 🔒
