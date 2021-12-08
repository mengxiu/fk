import random
import math
import cv2
import pyautogui
import time
import win32con
import win32gui
import  sys
import numpy as np
from PIL import ImageGrab

hwnd_title = {}
def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd))\
            and win32gui.GetWindowText(hwnd)=='阴阳师-网易游戏':
        hwnd_title.update({hwnd: win32gui.GetWindowRect(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)
print('共检测到',hwnd_title.__len__ (),'个阴阳师窗口')
def Image_Discern(imgone,imgtwo,locate=False):
    # 1.模板匹配
    # 大图

    img = np.asanyarray(imgone)

    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 小图
    template = np.asanyarray(imgtwo)
    # template=cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h, w = template.shape[:2]  # rows->h, cols->w


    # 对比图像
    res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

    # 返回坐标
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    min_val, _, min_loc, _ = cv2.minMaxLoc(res)
    # 计算中心坐标
    ###进行图像筛选###

    if min_val <= 0.03 :
        # print('图片匹配')
        if locate==True:
            return(True,min_loc)
        else:
            return (True)
    else:
        # print('图片不匹配')
        return(False,[0,0])





