#!/usr/bin/python3
################################################################################
# $Id: dnotify.py v1.0 2024-01-27 14:21:40 +0100 .m0rph $
################################################################################
# Description:
# ------------
#
# As a software developer it is very important to get periodic pauses,
# in order not to burn out. We have to get some good work / life balance,
# or it will somewhen be an unhealthy life, because we coders are vulnerable
# to addictional work behavior due to the fact that our coding challenges can
# be very enganging.
#
# So this is a little notifier, using the Windows notification service,
# reminding us to do a little break.
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

import time
from plyer import notification

if __name__ == '__main__':
   while True:
      notification.notify(
         title = 'ALERT !!!',
         message = 'Take a break! Already coding for three hours!',
         timeout = 10
      )
      time.sleep(3600 * 3) # seconds

