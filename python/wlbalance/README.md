# wlbalance — Work-Life Balance Notifier for Developers

**Author:** .m0rph  
**License:** [GNU GPLv3](https://gnu.org/licenses/gpl-3.0.html)  
**Language:** Python 3  
**Platform:** Linux / Windows / MSYS2 (Cross-platform)  
**Version:** 1.0

---

## 🧘 Purpose

As developers, we often get deeply absorbed in our work and lose track of time, leading to fatigue, poor sleep, or even burnout.  
This tool helps raise awareness of your daily cycle by:

- Logging when you got up, started/ended work, took breaks, or went to bed
- Reminding you to take breaks every 3 hours during active work periods
- Encouraging healthier routines for sustainable productivity

---

## 🚀 Features

- CLI-based time tracking for:
  - Waking up
  - Starting/ending work
  - Starting/ending breaks
  - Going to bed
- Logs stored in `~/.wlbalance.log`
- Status tracked in `~/.wlbalance.status`
- Automatic break reminder when `work begin` is active
- Fully systemd-compatible for Linux automation

---

## 🧰 Dependencies

Install `plyer` for cross-platform notifications:

### Kali/Debian/Ubuntu:
```bash
sudo apt install python3-plyer

