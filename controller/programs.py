import subprocess
import time


def is_xbmc_running():
    s = subprocess.Popen(["pidof", "xbmc.bin"], stdout=subprocess.PIPE, 
            close_fds=True)
    (out, err) = s.communicate()
    if out:
        return True
    return False

def start_xbmc():
    s = subprocess.Popen(["start-xbmc"], close_fds=True)
    s.communicate()
    # time.sleep(1)
    return is_xbmc_running()

def stop_xbmc():
    s = subprocess.Popen(["pidof", "xbmc.bin"], stdout=subprocess.PIPE, 
            close_fds=True)
    (pid, err) = s.communicate()
    pid = pid.strip()
    if not pid:
        return False

    s = subprocess.Popen(["kill", pid], close_fds=True)
    s.communicate()
    count = 0
    while is_xbmc_running() and count < 10:
        time.sleep(0.5)
        count += 1
        print count
    return is_xbmc_running()

def status():
    return {'xbmc': is_xbmc_running()}
