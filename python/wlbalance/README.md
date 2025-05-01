# wlbalance — Work-Life Balance Notifier for Developers

**Author:** .m0rph  
**License:** [GNU GPLv3](https://gnu.org/licenses/gpl-3.0.html)  
**Language:** Python 3  
**Platform:** Linux / Windows / MSYS2 (Cross-platform)  
**Version:** 1.0

---

## 🧘 Purpose

As developers, we often get deeply absorbed in our work and lose track of time, leading to fatigue, poor sleep, or even burnout. This cross-platform CLI tool helps us developers maintain a healthy work-life balance by tracking activity and reminding to take breaks regularly.

We now can raise awareness of our daily cycle by:

- Logging when you got up, started/ended work, took breaks, or went to bed
- Reminding you to take breaks every 3 hours during active work periods
- Encouraging healthier routines for sustainable productivity

---

## 🚀 Features

- CLI-based time tracking for:
  - Getting up
  - Starting/ending work
  - Starting/ending breaks
  - Going to bed
- Logs stored in `~/.wlbalance.log`
- Status tracked in `~/.wlbalance.status`
- Automatic break reminder when `work begin` is active
   - Configurable timer (e.g. every 3 hours)
- Cross-platform support: **Linux**, **Windows CMD**, **PowerShell**, **MSYS2 Zsh**
- Smart fallback to PowerShell toast notifications if `plyer` fails
- Fully systemd-compatible for Linux automation
- Runs in foreground or background (detached)

---

## 🧰 Dependencies

Install `plyer` for cross-platform notifications:

### Kali/Debian/Ubuntu:
```bash
sudo apt install python3-plyer notify-osd
```

### Windows (CMD, PowerShell, MSYS2) 

If using MSYS2, ensure Python is not the Windows-native one (**or use a venv**).

```bash
pip install plyer
```

---

## Usage

```bash
# Log actions
wlbalance.py -u                 # got up
wlbalance.py -d                 # went to bed
wlbalance.py -w begin           # start working
wlbalance.py -w end             # end working
wlbalance.py -p begin           # start pause
wlbalance.py -p end             # end pause
wlbalance.py -g                 # get current status

# Start notifier (blocks shell)
wlbalance.py --notifier

# Start notifier in background (detached, non-blocking)
wlbalance.py --detach-notifier

# Dry-run: show which notification backend would be used
wlbalance.py --test-notify

# Display version
wlbalance.py --version
```

---


## Log Format

All events are logged to .wlbalance.log with timestamps (local timezone):

```text
2025-04-30 03:29:46 +0200 work begin
```

***Have a lot of Fun ...***
