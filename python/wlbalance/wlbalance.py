#!/usr/bin/env python3
################################################################################
fid='$Id: wlbalance.py v1.8 2025-05-01 17:42:20 +0200 .m0rph $'
################################################################################
# Description:
# ------------
# As a developer it is absolutely importan to keep a good work/life balance,
# because we tend to addictive behavior. So this tool helps us track our sleep
# and work cycles. It records when you got up, started/ended work, took a break, 
# or went to bed. It also reminds you every 3 hours to take a break while
# working, helping to prevent burnout and support a healthy work-life balance.
#
# Have a lot of Fun ...
#
# .m0rph
# -----------------------------------------------------------------------------
#
# Dependencies:
#  system-wide: apt install python3-plyer (Debian based)
#   user-local: pip install plyer
#
#  % python wlbalance.py <option>(under Windows MSYS2)
#  % ./wlbalance.py <options>     (under Linux)
#
# Note: Blocks the shell
#  % python wlbalance.py --notifier (under Windows MSYS2)
#  % ./wlbalance.py --notifier      (under Linux)
#
# Note: Create detached subprocess
#  % python wlbalance.py --detach-notifier (under Windows MSYS2)
#  % ./wlbalance.py --detach-notifier      (under Linux)
#
################################################################################
# License: GNU/GPLv3 -- https://gnu.org/gpl-3.0
################################################################################
# No SheBand under Windows !!!

import argparse
import time
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone, timedelta
try:
    from plyer import notification
except ImportError:
    notification = None


SEP=os.path.sep
MYROOT = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.expanduser(f'{MYROOT}{SEP}.wlbalance.log')
STATUSFILE = os.path.expanduser(f'{MYROOT}{SEP}.wlbalance.status')
TZ = time.strftime('%z')
timer=3600 * 3 # sleep timer in seconds (three hours)

# Helper to write entry to log
def log_event(event: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f" {TZ}"
    with open(LOGFILE, 'a') as log:
        log.write(f"{timestamp} {event}\n")

# Helper to set current status
def set_status(state: str):
    with open(STATUSFILE, 'w') as f:
        f.write(state)

# Helper to get current status
def get_status():
    if not os.path.exists(STATUSFILE):
        return None
    with open(STATUSFILE, 'r') as f:
        return f.read().strip()

# Platform-aware notification
def notify(title, message, simulate=False):
    system = platform.system()
    if simulate:
        print(f"[SIMULATION] Would notify on {system}: '{title}' → {message}")
        return
    try:
        if system == "Windows" or system.startswith("MINGW"):
            print("[INFO] Using PowerShell fallback for Windows notifications.")
            subprocess.Popen([
                "powershell",
                "-WindowStyle", "Hidden",
                "-Command",
                f"[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime];"
                f"$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
                f"$template.GetElementsByTagName('text')[0].AppendChild($template.CreateTextNode('{title}')) > $null;"
                f"$template.GetElementsByTagName('text')[1].AppendChild($template.CreateTextNode('{message}')) > $null;"
                f"$toast = [Windows.UI.Notifications.ToastNotification]::new($template);"
                f"[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('wlbalance').Show($toast)"
            ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Linux":
            subprocess.Popen(["notify-send", title, message])
        elif system == "Darwin":
            subprocess.Popen(["osascript", "-e", f'display notification "{message}" with title "{title}"'])
        elif notification:
            notification.notify(title=title, message=message, timeout=10)
        else:
            print(f"[WARN] No usable notification backend for platform: {system}")
    except Exception as e:
        print(f"[WARN] Notification failed: {e}")

# Periodic notifier when in work mode
def run_notifier():
    print("[INFO] Notifier active: reminding every 3 hours while in 'work begin' mode.")
    try:
        while get_status() == "work begin" or get_status() == 'pause end':
            time.sleep(timer)
            notify(
                title='Take a break!',
                message='You have been working for 3 hours. Time to pause!'
            )
    except KeyboardInterrupt:
        print("[INFO] Notifier stopped by user.")

# One-time test of notification system (dry-run only)
def test_notify():
    print("[INFO] Running notification test (no message will be sent)...")
    notify("Test Notification", "This is a test of your notification system.", simulate=True)

# Start notifier in detached subprocess
def detach_notifier():
    print("[INFO] Detaching notifier into background process...")
    kwargs = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL
    }
    if os.name == 'nt': # True Windows environment
        kwargs["creationflags"] = 0x00000008 # DETACHED_PROCESS
    elif platform.system().startswith("MINGW"):
        #kwargs["creationflags"] = subprocess.DETACHED_PROCESS
        kwargs["stdin"] = subprocess.DEVNULL
    try:
      subprocess.Popen([sys.executable, __file__, "--notifier"], **kwargs)
      print("[INFO] Notifier launched in background.")
    except Exception as e:
      print(f"[ERROR] Could not launche detached notifier: {e}")
      


# Argument parsing
parser = argparse.ArgumentParser(description='Work-Life Balance Tracker',
    epilog='''
[en-US] Options:
-u, --up              := Log time you got up
-d, --down            := Log time you went to bed
-w, --work begin/end  := Start or end a work session
-p, --pause begin/end := Start or end a break session
--notifier            := Run periodic notifier (will block shell unless detached)
--detach-notifier     := Spawn notifier in separate detached background process
--test-notify         := Dry-run only; shows which backend would be used without sending a notification
''')

parser.add_argument('-v', '--version', action='version', version=('%s' % fid))
parser.add_argument('-u', '--up', action='store_true', help='Log time you got up')
parser.add_argument('-d', '--down', action='store_true', help='Log time you went to bed')
parser.add_argument('-w', '--work', choices=['begin', 'end'], help='Start or end working')
parser.add_argument('-p', '--pause', choices=['begin', 'end'], help='Start or end a pause')
parser.add_argument('--notifier', action='store_true', help='Run notifier in foreground')
parser.add_argument('--detach-notifier', action='store_true', help='Run notifier in background as subprocess')
parser.add_argument('--test-notify', action='store_true', help='Run a dry test without sending a notification')

args = parser.parse_args()

# Execution logic
if args.up:
    log_event("got up")
    set_status("idle")
elif args.down:
    log_event("layed down")
    set_status("asleep")
elif args.work:
    log_event(f"work {args.work}")
    set_status(f"work {args.work}")
elif args.pause:
    log_event(f"pause {args.pause}")
    set_status(f"pause {args.pause}")
elif args.notifier:
    if get_status() == 'work begin' or get_status() == 'pause end':
        run_notifier()
    else:
        print("[INFO] Not in 'work begin' status. Notifier not started.")
elif args.detach_notifier:
    if get_status() == 'work begin' or get_status() == 'pause end':
        detach_notifier()
    else:
        print("[INFO] Not in 'work begin' status. Notifier not detached.")
elif args.test_notify:
    test_notify()
else:
    parser.print_help()

