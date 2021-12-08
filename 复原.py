import win32gui
import win32api
import win32con
import pyautogui
import  time
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

hwnd_title = {}

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)
            and win32gui.GetWindowText(hwnd)=='阴阳师-网易游戏'):
        hwnd_title.update({hwnd: win32gui.GetWindowRect(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)
for hwnd, t in hwnd_title.items():
    if t :
        print (hwnd, t)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetForegroundWindow(hwnd)
time.sleep(3)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0,0,0,0,win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)
if __name__ == '__main__':
    pass