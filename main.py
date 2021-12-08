import time,sys,os
import keyboard
import win32com.client
from Wins1 import *
from myutils import read_config
time.sleep(0.1)
accounts = []
_isPaused = False
count = 0
config_file_name='huntu.ini'
if len(sys.argv)>1 :
    config_file_name=sys.argv[1]
    # if sys.argv[1] == 'no_rest':
    #     conf['main'].update({'rest':'no'})
    # if sys.argv[1] == 'rest':
    #     conf['main'].update({'rest':'yes'})
conf=read_config(config_file_name=config_file_name)


def get_all_hwnd():
    win_list = []
    hwnd = win32gui.FindWindowEx(None, 0, None, '阴阳师-网易游戏')
    while (True):
        if hwnd == 0:
            break
        if (win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd)):
            win_list.append([hwnd, win32gui.GetWindowPlacement(hwnd)[4]])
        hwnd = win32gui.FindWindowEx(None, hwnd, None, '阴阳师-网易游戏')
    for i in range(len(win_list)):
        for j in range(i, len(win_list)):
            if win_list[i][0] < win_list[j][0]:
                win_list[i], win_list[j] = win_list[j], win_list[i]

    return win_list


def get_accounts():
    global conf
    print("注意:请务必使用'管理员权限'运行!")
    win_list = get_all_hwnd()  # 获取阴阳师窗口句柄，以及两个顶点的坐标
    print('共检测到', win_list.__len__(), '个阴阳师窗口')
    for yyswin in win_list:
        winHwnd = yyswin[0]
        winRect = yyswin[1]
        # assert isinstance(winRect, object)

        print('///////////////////////////////////')
        print('窗口:', winHwnd, winRect)
        # whetherAdd=inputWithTimePrompt('是否添加(Y/N)')

        startX = winRect[0]
        startY = winRect[1]
        endX = winRect[2]
        endY = winRect[3]

        win32gui.ShowWindow(winHwnd, 9)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(winHwnd)
        time.sleep(0.5)
        accounts.append(HunTu(winHwnd, startX, startY, endX, endY,conf['main']['filename']))


def rest():
    global conf
    global count
    count += 1
    print('\r', '已经循环了{}次'.format(count), end='')
    if count > random.randint(30, 40) and conf['main']['rest']=='yes':
        count = 0
        print('\n休息一下吧')
        time.sleep(40+random.randint(10,20))


class detect_pause(threading.Thread):
    def __init__(self):
        super(detect_pause, self).__init__()

    def run(self) -> None:
        global _isPaused
        while True:
            print("开始监控f12")
            keyboard.wait(hotkey='f12')
            print("\n正在暂停")
            _isPaused = True
            keyboard.wait(hotkey='f12')
            _isPaused = False
            print("\n已重新开始")


def huntu():
    global accounts, _isPaused,conf
    stop_flag=False
    while True:
        rest()
        for i in accounts:
            while _isPaused:
                time.sleep(0.1)

            i.HunTu_start()
        time.sleep(float(conf['main']['time']))
        for i in accounts:
            while _isPaused:
                time.sleep(0.1)
            if i.HunTu_over():
                stop_flag=True
        if stop_flag:
            for i in accounts:
                while _isPaused:
                    time.sleep(0.1)
                i.close_jiacheng()
            break

pau = detect_pause()
pau.start()
get_accounts()
huntu()
if conf['other']['shutdown_game']=='True':
    os.system('taskkill /f /t /im onmyoji.exe')
pau.join()
