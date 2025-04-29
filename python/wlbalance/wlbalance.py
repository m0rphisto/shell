#!/usr/bin/env python3
################################################################################
# $Id: wlbalance.py v1.0 2025-04-30 01:21:27 +0200 .m0rph $
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
# Note: Run in background 
#
#  % python notify.py & (under Windows MSYS2)
#  % ./notify.py &      (under Linux)
#
################################################################################
# License: GNU/GPLv3 -- https://gnu.org/gpl-3.0
################################################################################
# No Shebang line under Windows !!!

import argparse
import time
import os
from datetime import datetime, timezone, timedelta
from plyer import notification

LOGFILE = os.path.expanduser("~/.wlbalance.log")
STATUSFILE = os.path.expanduser("~/.wlbalance.status")
TZ = time.strftime('%z')

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

# Periodic notifier when in work mode
def run_notifier():
    print("[INFO] Notifier active: reminding every 3 hours while in 'work begin' mode.")
    try:
        while get_status() == "work begin":
            notification.notify(
                title='Take a break!',
                message='You have been working for 3 hours. Time to pause!',
                timeout=10
            )
            time.sleep(3600 * 3)
    except KeyboardInterrupt:
        print("[INFO] Notifier stopped by user.")

# Argument parsing
parser = argparse.ArgumentParser(description='Work-Life Balance Tracker',
    epilog='''
Options:
-u, --up              := got up
-d, --down            := layed down
-w, --work begin/end  := start or end working
-p, --pause begin/end := start or end a pause
--notifier            := run notifier in background while working
''')

parser.add_argument('-v', '--version', action='version', version='wlbalance v1.0')
parser.add_argument('-u', '--up', action='store_true', help='[en-US] Log time you got up')
parser.add_argument('-d', '--down', action='store_true', help='[en-US] Log time you went to bed')
parser.add_argument('-w', '--work', choices=['begin', 'end'], help='[en-US] Start or end working')
parser.add_argument('-p', '--pause', choices=['begin', 'end'], help='[en-US] Start or end a pause')
parser.add_argument('--notifier', action='store_true', help='[en-US] Run notifier in background')

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
    if get_status() == 'work begin':
        run_notifier()
    else:
        print("[INFO] Not in 'work begin' status. Notifier not started.")
else:
    parser.print_help()

