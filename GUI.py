import cv2
import pyautogui
import threading
import time
import random
import os
from myutils import pilImage2ndarray

_GUILocker = threading.Lock()

method_list = [pyautogui.easeInBounce, pyautogui.easeOutQuad, pyautogui.easeOutQuad, pyautogui.easeOutSine]


class GUI(object):

    def __init__(self, startX, startY, windowWidth, windowHeight):
        self.startX = startX
        self.startY = startY
        self.__windowWidth = windowWidth
        self.__windowHeight = windowHeight
        self.__image_dict = {}

    def image_locate(self, image_path):
        # 返回要匹配图片在屏幕中的位置,找不到则return false
        global imaimage_dict
        abs_path = os.path.abspath(image_path)
        image1 = cv2.imread(image_path, 0)
        image2 = pyautogui.screenshot(
            region=[self.startX, self.startY, self.__windowWidth, self.__windowHeight])
        image2 = pilImage2ndarray(image2)
        if (abs_path not in self.__image_dict.keys()):
            rect = self.match(image1, image2, return_rect=True)
            if rect==False:
                return False
            rect[0] = rect[0] + self.startX
            rect[1] = rect[1] + self.startY
            rect[2] = rect[2] + self.startX
            rect[3] = rect[3] + self.startY
            self.__image_dict.update({abs_path: rect})
        recttmp=self.__image_dict.get(abs_path).copy()
        recttmp[0] = recttmp[0] - self.startX
        recttmp[1] = recttmp[1] - self.startY
        recttmp[2] = recttmp[2] - self.startX
        recttmp[3] = recttmp[3] - self.startY
        if self.match(image1,image2[max(recttmp[1]-10,0):min(recttmp[3]+10,image2.shape[0]),max(recttmp[0]-10,0):min(recttmp[2]+10,image2.shape[1]),:])==False:
            return False
        return self.__image_dict.get(abs_path)

    def find_and_click(self, image_path):
        #找图片点击，没有就return false
        img_loc = self.image_locate(image_path)
        if img_loc == False:
            return False
        x = random.randint(img_loc[0], img_loc[2])
        y = random.randint(img_loc[1], img_loc[3])
        self.click( x, y)
        return True

    def click(self, x, y):
        global method_list
        # x0, y0 = pyautogui.position()
        # if (x - x0) ** 2 + (y - y0) ** 2 > 250000:
        #     x1 = random.randint(x0, x)
        #     y1 = random.randint(y0, y)
        #     pyautogui.moveTo(x1, y1, random.uniform(0.15, 0.3), random.choice(method_list))
        pyautogui.moveTo(x, y, random.uniform(0.15, 0.3), random.choice(method_list))
        pyautogui.click()

    def match(self,img1, img2, return_rect=False):
        if len(img1.shape)==3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        if len(img2.shape) == 3:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        h, w = img2.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF_NORMED)

        # 返回坐标
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)
        rect = list(min_loc)
        rect.append(rect[0] + img1.shape[1])
        rect.append(rect[1] + img1.shape[0])

        if min_val <= 0.03:
            # print('图片匹配')
            if return_rect == True:
                return rect
            return (True)
        else:
            # print('图片不匹配')
            return (False)