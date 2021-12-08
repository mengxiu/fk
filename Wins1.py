import win32gui
import win32com.client


from GUI import *


count = 0

_detectPauseThread = threading.Thread()
_accountLocker = threading.Lock()
_isPaused = False

class HunTu():
    def __init__(self, winHwnd, startX, startY, endX,endY,dir_name='huntu'):
        global _detectPauseThread
        self.__startX = startX
        self.__startY = startY
        self.__winHwnd = winHwnd
        self.__windowWidth =endX- startX
        self.__windowHeight = endY-startY
        self.__endX = endX
        self.__endY = endY
        self.__isCaptain = False
        self.__dir_name=dir_name
        self.__gui = GUI(startX, startY, self.__windowWidth, self.__windowHeight)




    def HunTu_start(self):
        self.ative()
        time.sleep(0.05)
        count=0
        start_pic_list = []
        dir = os.path.abspath('./' + self.__dir_name + '/start')
        for x in os.listdir(dir):
            path = os.path.join(dir, x)
            if os.path.isfile(path):
                start_pic_list.append('./' + self.__dir_name + '/start/' + x)
        while self.__gui.find_and_click(random.choice(start_pic_list))!=False:
            #不要删掉！=false或者改成==true，因为返回值还可能是其他
            time.sleep(0.2)
            count = count + 1
            if count > 6:
                self.__gui.find_and_click('./expect/xuanshang2.png')
                time.sleep(0.1)
                self.__gui.find_and_click('./expect/xuanshang.png')
                count = 0
        time.sleep(0.1)
    def expect_solve(self)->bool:
        self.__gui.find_and_click('./expect/xuanshang2.png')
        time.sleep(0.55)
        self.__gui.find_and_click('./expect/xuanshang.png')
        if self.__gui.find_and_click('./expect/yuhun_man.png'):
            return True
        return False
    def HunTu_over(self)->bool:
        self.ative()

        stop_flag = False

        # str = 'over'
        # over_pic_list = []
        # dir = os.path.abspath('./huntu')
        # for x in os.listdir(dir):
        #     path = os.path.join(dir, x)
        #     if os.path.isfile(path) and str in os.path.splitext(x)[0]:
        #         #这句判断是否是文件，以及文件名包不包含‘over'
        #         over_pic_list.append('./huntu/' + x)
        #获取结束区域图片的名称列表



        over_pic_list = []
        dir = os.path.abspath('./'+self.__dir_name+'/over')
        for x in os.listdir(dir):
            path = os.path.join(dir, x)
            if os.path.isfile(path):
                over_pic_list.append('./'+self.__dir_name+'/over/' + x)
        confirm_pic_list = []
        dir = os.path.abspath('./' + self.__dir_name + '/confirm')
        for x in os.listdir(dir):
            path = os.path.join(dir, x)
            if os.path.isfile(path):
                confirm_pic_list.append('./' + self.__dir_name + '/confirm/' + x)


        count=0
        while (1):
            if any(list(map(lambda x:self.__gui.image_locate(x),confirm_pic_list))):
                break
            if self.__dir_name=='huntu':
                self.__gui.find_and_click('./huntu/huntu_end.png')
            time.sleep(0.1+random.random()*0.2)
            self.__gui.find_and_click(random.choice(over_pic_list))
            count = count + 1
            if count > 6:
                stop_flag=self.expect_solve()
                count=0
        time.sleep(0.1)
        return stop_flag




    def ative(self):
        win32gui.ShowWindow(self.__winHwnd, 9)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.__winHwnd)
        time.sleep(0.1+random.random()*0.12)
        self.__gui.click(self.__startX + 100+random.randint(100,800), self.__startY + 15+random.randint(0,8))
        self.__gui.click(self.__startX + 100 + random.randint(100, 800), self.__startY + 15 + random.randint(0, 8))
        time.sleep(0.2)
    def close_jiacheng(self):
        self.ative()
        rect=self.__gui.image_locate('./expect/jiacheng2.png')
        if self.__gui.find_and_click('./expect/jiacheng2.png')!=False:
            if rect!=False:
                from myutils import read_config
                conf_temp = read_config()
                length_short=int(conf_temp['jiacheng']['short'])
                length_long=int(conf_temp['jiacheng']['long'])
                x=random.randint(rect[0],rect[2])
                y=random.randint(rect[3]+length_short,rect[3]+length_long)
                time.sleep(0.8)
                self.__gui.click(x,y)

