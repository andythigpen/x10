from log import get_log
import subprocess
import time
import os
import re

log = get_log("programs")

xbmc_kill_count = 0

def is_xbmc_running():
    s = subprocess.Popen(["pidof", "xbmc.bin"], stdout=subprocess.PIPE, 
            close_fds=True)
    (out, err) = s.communicate()
    if out:
        return True
    return False

def start_xbmc():
    s = subprocess.Popen(["/usr/sbin/start-xbmc"], close_fds=True)
    s.communicate()
    return is_xbmc_running()

def stop_xbmc():
    global xbmc_kill_count
    s = subprocess.Popen(["pidof", "xbmc.bin"], stdout=subprocess.PIPE, 
            close_fds=True)
    (pid, err) = s.communicate()
    pid = pid.strip()
    if not pid:
        return False

    cmd = ["kill", pid]
    if xbmc_kill_count >= 2:
        cmd = ["kill", "-9", pid]

    s = subprocess.Popen(cmd, close_fds=True)
    s.communicate()
    count = 0
    while is_xbmc_running() and count < 10:
        time.sleep(0.5)
        count += 1
        print count
    if is_xbmc_running():
        xbmc_kill_count += 1
    else:
        xbmc_kill_count = 0
    return is_xbmc_running()

def status():
    return {'xbmc': is_xbmc_running(), 'power': power_status()}


#
# To use the power functionality, the user executing the daemon should have
# sudo privileges with no password for the shutdown command
#
JOBS_FILE = "%s/at.jobs" % os.path.realpath(os.path.dirname(__file__))
def clear_power():
    if not os.path.exists(JOBS_FILE):
        return True

    log.debug("clearing atq")
    f = open(JOBS_FILE, 'r')
    job = f.read()
    f.close()
    if job:
        s = subprocess.Popen(["atrm", job.strip()])
        s.communicate()

    try:
        os.remove(JOBS_FILE)
    except OSError:
        pass
    return True

def shutdown_pc(when='0'):
    clear_power()
    log.debug("shutdown_pc when=%s" % when)
    s = subprocess.Popen(["at", "now", "+", when, "minutes"], 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    (out, err) = s.communicate("sudo shutdown -h now")
    for line in out.splitlines():
        match = re.match(r'job (\d+)', line)
        if match:
            f = open(JOBS_FILE, 'w')
            f.write(match.group(1))
            f.close()
            return True

    return False

def restart_pc(when='now'):
    clear_power()
    log.debug("restart_pc when=%s" % when)
    s = subprocess.Popen(["at", "now", "+", when, "minutes"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    (out, err) = s.communicate("sudo shutdown -r now")
    for line in out.splitlines():
        match = re.match(r'job (\d+)', line)
        if match:
            f = open(JOBS_FILE, 'w')
            f.write(match.group(1))
            f.close()
            return True

    return True

def power_status():
    if not os.path.exists(JOBS_FILE):
        return ""

    f = open(JOBS_FILE, 'r')
    job = f.read()
    f.close()

    if not job.strip():
        return ""

    log.debug("power_status job=%s" % job)
    action = ""
    time = ""
    s = subprocess.Popen(["at", "-c", job.strip()], stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    (out, err) = s.communicate()
    for line in out.splitlines():
        match = re.match(r'sudo shutdown -(h|r){1}', line)
        if match:
            if match.group(1) == "h":
                action = "Shutdown"
            elif match.group(1) == "r":
                action = "Restart"
            break
        # clear out the JOB_FILE if the job doesn't exist anymore
        match = re.match(r'Cannot find job', line)
        if match:
            log.debug("Job not found")
            clear_power()

    s = subprocess.Popen(["atq"], stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    (out, err) = s.communicate()
    for line in out.splitlines():
        match = re.match(r'(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+([\d:]+)', line)
        if match and match.group(1) == job.strip():
            time = "%s %s %s %s" % (match.group(2), match.group(3), 
                    match.group(4), match.group(5))
            break

    log.debug("action=%s time=%s" % (action,time))
    if action and time:
        return "%s at %s" % (action, time)
    return ""

