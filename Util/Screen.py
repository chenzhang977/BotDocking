# use 'pip install pywin32' to install
import win32api, win32con, win32gui 
from PIL import Image, ImageGrab
import pygetwindow as gw

def get_window_pos(name):
    name = name
# 获取指定进程的窗口句柄
    handle = gw.getWindowsWithTitle(name)[0]
    #handle = win32gui.FindWindow(None, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle


def fetch_image():
    (x1, y1, x2, y2), handle = get_window_pos('cmd')
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 截图
    grab_image = ImageGrab.grab((x1, y1, x2, y2))
    
    return grab_image