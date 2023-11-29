import threading
import time

interval = 1
lock = threading.Lock()

def periodic_func(func):
    while True:
        with lock:
            func()
            time.sleep(interval)

def start_loop(func):
    thread = threading.Thread(target=periodic_func, args=(func,))
    thread.daemon = True
    thread.start()
