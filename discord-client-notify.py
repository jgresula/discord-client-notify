#!/usr/bin/env python3

import subprocess
import re
import time

cooldown_ = 5

rex_title = re.compile('Discord$')
def discord_window_id():
    out = subprocess.check_output(["wmctrl", "-l"]).decode('utf-8')
    for line in out.split("\n"):
        if rex_title.search(line):
            return line.split(' ', 1)[0]

rex_current = re.compile('window id # (0x[a-f0-9]+)')
def current_window_id():
    out = subprocess.check_output(
        ["xprop", "-root", "_NET_ACTIVE_WINDOW"]).decode('utf-8')
    return rex_current.search(out).group(1)
    

def notify():
    current_id = current_window_id()
    discord_id = discord_window_id()
    if discord_id:
        subprocess.run(['wmctrl', '-i', '-R', discord_id])
        subprocess.run(['wmctrl', '-i', '-R', current_id])
    else:
        print("Err: Discord window not found!")
    

def run_forever():
    # https://askubuntu.com/a/770249
    with subprocess.Popen(['dbus-monitor',
                "interface='org.freedesktop.Notifications'"],
               stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        last = 0
        for line in p.stdout:
            if 'discord' in line.lower():
                if time.time()-last > cooldown_:
                    notify()
                    last = time.time()

if __name__ == "__main__":
    run_forever()

