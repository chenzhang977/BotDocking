import subprocess
import traceback

def run_bat(path: str, cwd: str = None)->int:
    stack = subprocess.Popen(path,cwd = cwd)
    return stack.pid

def run_cmd(cmd: str, cwd: str = None):
    try:
        result = subprocess.run(cmd, text = True, shell = True, capture_output = True, cwd = cwd)
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