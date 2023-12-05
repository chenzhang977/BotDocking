import subprocess
import traceback

def run_bat(path: str)->int:
    stack = subprocess.Popen(path)
    return stack.pid

def run_cmd(cmd: str):
    try:
        result = subprocess.run(cmd, text = True)
        return result
    except Exception as e:
        s = traceback.format_exc()
        print(e)
        print(s)
        return None

def is_run(pid: int)->bool:
    result = run_cmd(f'tasklist /FI \"PID eq {pid}\"')
    return result and result.returncode == 0 or False

def kill(pid: int)->bool:
    result = run_cmd(f'taskkill /F /PID {pid}')
    return result and result.returncode == 0 or False