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


def monitor_and_restart(logfile: str, command: str, time_interval: int):
    """
    Monitors the modified time of a logfile. If it exceeds the time_interval,
    it kills the process with the given command and restarts it.
    
    :param logfile: Path to the log file.
    :param command: Command line of the process to monitor.
    :param time_interval: Time in seconds before considering the process stuck.
    """

    while True:
        last_modified = get_last_modified_time(logfile)
        current_time = time.time()
        
        if current_time - last_modified > time_interval:
            print(f"Logfile {logfile} is stale. Restarting process...")
            restart_process(command=command)

        time.sleep(5)


if __name__ == '__main__':
    logfile = 'logs/cam.log'
    command = 'python test.py cam1'
    time_interval = 5

    monitor_and_restart(logfile, command, time_interval)
