import cv2
import threading
import iten_model.Config as Config
from utils import log
import datetime as dt
import os

class Vision(object):
    def __init__(self, camera):
        self.position = 0  # 位置坐标
        self.__recording = False  # 是否录像
        self.__frame = None
        self.__frame_rec = None
        self.__next_frame = False
        try:
            log.log('正在初始化相机')
            self.__camera = cv2.VideoCapture(0)
            log.log('正在调定相机参数')
            self.__camera.set(3, Config.FRAME_WIDTH)
            self.__camera.set(4, Config.FRAME_HEIGHT)
            log.log('相机初始化完成')
            video_observ_thread = threading.Thread(target=self.__observ)
            video_observ_thread.start()
        except:
            log.log('相机初始化失败，视觉部分无法正常工作')

    def __observ(self):
        # 图像分析线程
        log.log('图像分析线程开始工作')
        fgbg = cv2.createBackgroundSubtractorMOG2(history=20)
        while True:
            _, self.__frame = self.__camera.read()
            # print(self.__frame.shape)
            if not self.__next_frame:
                self.__frame_rec = self.__frame.copy()
                self.__next_frame = True
            fgmask = fgbg.apply(self.__frame)
            _, after_threshold = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
            after_gaussianblur = cv2.GaussianBlur(after_threshold, (5, 5), 0)
            _, threshold_again = cv2.threshold(after_gaussianblur, 200, 255, cv2.THRESH_BINARY)
            _, _, _, position = cv2.minMaxLoc(threshold_again)
            self.position = position
            cv2.waitKey(10)

    def record(self, user_id, length=Config.REC_LENGTH, freq=Config.REC_FREQ):
        def record_thread(user_id, length=Config.REC_LENGTH, freq=Config.REC_FREQ):
            self.__recording = True
            path = os.getcwd()
            path = os.path.join(path, 'video_cache')
            dirname = user_id+str(dt.datetime.now().timestamp())
            path = os.path.join(path, dirname)
            print(path)
            os.mkdir(path)
            filepath = os.path.join(path, 'video.avi')
            video_writer = cv2.VideoWriter(filepath, -1, 12, (Config.FRAME_WIDTH, Config.FRAME_HEIGHT))
            print(Config.FRAME_WIDTH, Config.FRAME_HEIGHT)
            for i in range(length):
                while not self.__next_frame:
                    pass
                if self.__frame_rec.shape == (Config.FRAME_HEIGHT, Config.FRAME_WIDTH, 3):
                    video_writer.write(self.__frame_rec)
                    print(self.__frame_rec.shape)
                self.__next_frame = False
            video_writer.release()
            self.__recording = False
        if not self.__recording:
            threading.Thread(target=record_thread, args=(user_id, length, freq)).start()



    def __convert_upload(self):
        pass





