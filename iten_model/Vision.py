
import threading

class Vision(object):
    def __init__(self, camera):
        self.position = 0  # 位置坐标
        self.__recording = False  # 是否录像

