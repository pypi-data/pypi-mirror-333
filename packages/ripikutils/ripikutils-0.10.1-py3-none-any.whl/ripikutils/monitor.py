import os
import time
import subprocess
import psutil


def get_last_modified_time(file_path: str):
    """Returns the last modified time of the given file."""
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return 0

def find_process_by_command(cmd: str):
    """Finds a process by its command and returns a list of matching PIDs."""
    matching_pids = []
    for proc in psutil.process_iter(attrs=["pid", "cmdline"]):
        try:
            if proc.info["cmdline"] and " ".join(proc.info["cmdline"]) == cmd:
                matching_pids.append(proc.info["pid"])
        except psutil.NoSuchProcess:
            continue
    return matching_pids

def restart_process(command: str):
    """Kills the process and starts a new one."""
    pids = find_process_by_command(command)
    for pid in pids:
        print(f"Killing process {pid}...")
        try:
            psutil.Process(pid).terminate()
            time.sleep(2)
            if psutil.pid_exists(pid):
                psutil.Process(pid).kill()
        except psutil.NoSuchProcess:
            pass

    print(f"Restarting process: {command}")
    subprocess.Popen(command, shell=True)


def kill_process(command: str):
    """Kills the process."""
    pids = find_process_by_command(command)
    for pid in pids:
        print(f"Killing process {pid}...")
        try:
            psutil.Process(pid).terminate()
            time.sleep(2)
            if psutil.pid_exists(pid):
                psutil.Process(pid).kill()
        except psutil.NoSuchProcess:
            pass


def monitor_and_restart(logfile: str, command: str, time_interval: int, first_run: bool = True):
    """
    Continuously monitors a logfile and restarts the associated process if the file becomes stale.

    This function implements a monitoring loop that checks the last modification time of a logfile.
    If the file hasn't been modified for longer than the specified time interval, it considers
    the process as stale and automatically restarts it. The monitoring continues indefinitely.

    Args:
        logfile (str): Path to the log file to monitor
        command (str): Shell command to execute when starting/restarting the process
        time_interval (int): Maximum time in seconds allowed between log file updates
        first_run (bool): If True, starts the process immediately before beginning monitoring. Defaults to `True`.
    """

    if first_run:
        restart_process(command=command)
        time.sleep(10)

    while True:
        last_modified = get_last_modified_time(logfile)
        current_time = time.time()
        
        if current_time - last_modified > time_interval:
            print(f"Logfile {logfile} is stale. Restarting process...")
            restart_process(command=command)

        time.sleep(5)


def monitor_and_kill(logfile: str, command: str, time_interval: int, first_run: bool = True):
    """
    Monitors a logfile for activity and terminates a process if the logfile becomes stale.

    This function continuously monitors the specified logfile's last modification time.
    If the file hasn't been modified for longer than the specified time interval,
    it considers the process as stale and terminates it using the provided command.
    The function will exit after killing the process.

    Args:
        logfile (str): Path to the log file to monitor
        command (str): Shell command used to identify the process to kill
        time_interval (int): Maximum time in seconds allowed between log file updates
        first_run (bool): If True, starts the process initially before monitoring. Defaults to `True`.
    """


    if first_run:
        restart_process(command=command)
        time.sleep(10)

    while True:
        last_modified = get_last_modified_time(logfile)
        current_time = time.time()

        if current_time - last_modified > time_interval:
            print(f"Logfile {logfile} is stale. Killing process...")
            kill_process(command=command)
            return

        time.sleep(5)


if __name__ == '__main__':
    logfile = 'logs/cam.log'
    command = 'python test.py cam1'
    time_interval = 5

    monitor_and_restart(logfile, command, time_interval)
