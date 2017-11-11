import serial
from utils import log

class Device(object):
    def __init__(self, com):
        self.com = com
        self.args = {}

    def shoot(self, machine, point, director):
        # TODO 发球指令
        log.log('发球')
        pass

    def start(self):
        log.log('启动网球机')
        # TODO 网球机启动指令
        pass

    def stop(self):
        # TODO 网球机终止指令
        log.log('停止网球机运行')
        pass
