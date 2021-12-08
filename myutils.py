import cv2
import numpy as np

def pilImage2ndarray(ori_img):
    return (cv2.cvtColor(np.asanyarray(ori_img), cv2.COLOR_RGB2BGR))
def read_config(config_file_name:str='huntu.ini'):
    import configparser
    conf=configparser.ConfigParser()
    conf.read(config_file_name)
    res={}
    for sec in conf.sections():
        section={}
        for item in conf.items(sec):
            section.update({item[0]:item[1]})
        res.update({sec:section})
    return res

